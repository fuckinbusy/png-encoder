from os import stat
import os
from struct import pack
from Converter import bytesInt, bytesStr, bytesHEX, generateCRC

def encode(filePath: str, fileToHide: str):
    """Encodes fileToHide in filePath"""
    print("----------ENCODER----------")
    if filePath.split(".")[-1] != "png":
        print("Not a png file")
        return
    
    with open(filePath, 'rb+') as png:
        png.seek(os.stat(filePath).st_size - 4)
        EOF_LAST_4_BYTES = png.read()
        png.seek(0)
        png.read(8) 
        chunk_type = "IHDR"

        while chunk_type != "IEND":
            size = bytesInt(png.read(4))
            type_ = bytesStr(png.read(4))

            if type_ == "riCH":
                print("File already encoded.")
                return

            if type_ == "IEND":
                png.seek(-8, 1)
                offset = png.tell()
                richSize, richCRC = stat(fileToHide).st_size, generateCRC(fileToHide)

                #Write SIZE of chunk
                png.write(pack("!i", richSize))

                #Write chunk TYPE
                png.write(bytearray("riCH", 'ascii'))

                #Write data
                secret = open(fileToHide, 'rb')
                secretbytes = secret.read()
                secret.close()
                png.write(secretbytes)

                #Write chunk CRC
                crc = pack("!I", richCRC)
                png.write(bytearray(crc))

                #Write new IEND chunk
                png.write(bytearray(pack('!i', 0)))
                png.write(bytearray("IEND", 'ascii'))
                png.write(EOF_LAST_4_BYTES)

                """
                I have no idea what are the last 4 bytes after IEND.
                WIKI: IEND marks the image end; the data field of the IEND chunk has 0 bytes/is empty.
                So no information about last 4 bytes, but maybe im just blind or too lazy to read.

                I checked a lot of png files and it seems that they all have the same last 4 bytes
                and here they are -> AE 42 60 82
                """

                print(f"riCH chunk ({richSize} bytes) injected at {hex(offset)}")
                break
            else:
                png.read(size)
                bytesHEX(png.read(4))
                chunk_type = type_

def decode(filePath: str, newFile: str) -> str:
    """Decodes secret data from PNG file.\nReturns decoded file path."""
    print("----------DECODER----------")
    with open(filePath, 'rb') as file:
        file.read(8)
        chunk_type = "IHDR"
        while chunk_type != "IEND":
            size = bytesInt(file.read(4))
            type_ = bytesStr(file.read(4))
            chunk_type = type_

            if type_ == "riCH":
                print(f"Secret data found ({size} bytes). Decoding...")
                secretData = file.read(size)
                new = open(newFile, "wb")
                new.write(bytearray(secretData))
                print(f"Decoded into {new.name}")
                new.close()
                return os.path.abspath(new.name)
            else:
                file.read(size)
                bytesHEX(file.read(4))

                
    print("Secret data not found!")

def iterChunks(filePath):
    """Iterates through chunks to check if riCH chunk exists"""
    print("----------CHECKER----------")
    chunks = []
    with open(filePath, 'rb') as png:
        png.read(8)
        print("Searching for new chunk...")
        chunk = "IHDR"

        while chunk != "IEND":
            size = bytesInt(png.read(4))
            type_ = bytesStr(png.read(4))
            chunk = type_
            png.read(size)
            crc = bytesHEX(png.read(4))
            chunks.append(type_)
            print(size, type_, crc, "\n",sep="\n")

    if "riCH" in chunks:
            print("riCH chunk found. Injection success!")  