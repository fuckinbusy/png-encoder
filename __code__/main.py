"""
http://www.libpng.org/pub/png/spec/1.2/PNG-Contents.html
https://www.w3.org/TR/2003/REC-PNG-20031110/

WIKI EN: https://en.wikipedia.org/wiki/PNG

HOW DOES IT WORK:

PNG chunk struct --->

first 8 bytes of PNG is just a file signature

---------------------------------------STARTOFFILE
Start of file            | 8 bytes
---------------------------------------CHUNK "IHDR" - this chunk always go first as it contains image attributes like 'width', 'height' etc.
13 - size of chunk data  | 4 bytes long
IHDR - chunk type        | 4 bytes long
*data* - data of chunk   | 13 bytes long
1a3057f6 - chunk crc     | 4 bytes long
---------------------------------------ENDOFCHUNK
---------------------------------------CHUNK
? - size of chunk data  | 4 bytes long
? - chunk type        | 4 bytes long
*data* - data of chunk   | *value of size* bytes long
HEX - chunk crc     | 4 bytes long
---------------------------------------ENDOFCHUNK
---------------------------------------CHUNK
? - size of chunk data  | 4 bytes long
? - chunk type        | 4 bytes long
*data* - data of chunk   | *value of size* bytes long
HEX - chunk crc     | 4 bytes long
---------------------------------------ENDOFCHUNK
---------------------------------------CHUNK "IEND" - this chunk always at the end. It marks the image end; the data field of the IEND chunk has 0 bytes/is empty.
0 - size of chunk data  | 4 bytes long
IEND - chunk type        | 4 bytes long
0 - data of chunk   | no data - no bytes, so this doesnt exists
HEX - chunk crc     | no data - no bytes, so this doesnt exists
---------------------------------------ENDOFCHUNK
---------------------------------------ENDOFFILE

so you can see we can easily modife png by adding our custom chunks with any data that we want
you can even put another image into the chunk data, so your image will be stored inside another image

one chunk can handle about 2gb of data

each section of chunk has size of 4 bytes except data

The CRC (Cyclic Redundancy Check) - a network-byte-order CRC-32 computed over the chunk type and chunk data, but not the length.
WIKI EN: https://en.wikipedia.org/wiki/Cyclic_redundancy_check
WIKI RU: https://ru.wikipedia.org/wiki/Циклический_избыточный_код

---------------------------------------Iterate through PNG chunks
with open("image.png", 'rb+') as png:
    first8bytes = png.read(8)
    chunk_type = "IHDR"
    end_chunk = "IEND"
    while chunk_type != end_chunk:
        size = bytesInt(png.read(4))
        type_ = bytesStr(png.read(4))
        data = png.read(size)
        crc = bytesHEX(png.read(4))
        chunk_type = type_
        print(size, type_, crc, "\n",sep="\n")

"""


from Encoder import iterChunks, encode, decode
from tkinter import filedialog as fd
from os import system

def main():
    while True:
        choice = input("Choose an option: 1-Encode, 2-Decode, 3-Quit: ").lower()
        system('cls')
        if choice == "1" or choice == "encode":
            print("PNG file container: ", end=' ')

            try:
                filePath = fd.askopenfile(title="Choose PNG file:",
                                          filetypes=[("PNG file container", "*.png")]).name
            except TypeError:
                print("choose a file!")
                continue
            except AttributeError:
                print("choose a file!")
                continue

            print(filePath)
            print("File that will be encoded:", end=' ')

            try:
                fileToHide = fd.askopenfile(title="Choose any file that will be encoded: ").name
            except TypeError:
                print("choose a file!")
                continue
            except AttributeError:
                print("choose a file!")
                continue

            print(fileToHide)
            encode(filePath, fileToHide)
            iterChunks(filePath)


        elif choice == "2" or choice == "decode":
            print("PNG file to decode:", end=' ')

            try:
                filePath = fd.askopenfile(title="Choose a PNG file to decode:",
                                          filetypes=[("PNG file to decode", "*.png")]).name
            except TypeError:
                print("choose a file!")
                continue
            except AttributeError:
                print("choose a file!")
                continue
            
            print(filePath)
            newFile = input("Decoded file name with extension: ", )
            decoded_path = decode(filePath, newFile)
            if not decoded_path == None:
                print(f"Decoded file saved as {decoded_path}")


        elif choice == "3" or choice == "quit":
            print("app closed")
            return


if __name__ == "__main__":
    main()
