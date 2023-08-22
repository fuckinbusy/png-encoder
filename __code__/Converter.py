from binascii import crc32
from os import stat

def bytesInt(bytes: bytes) -> int:
    """Converts bytes to int"""
    return int.from_bytes(bytes, "big")

def bytesStr(bytes: bytes) -> str:
    """Converts bytes to string"""
    return bytes.decode("utf-8")

def bytesHEX(bytes: bytes) -> str:
    """Converts bytes to hex string"""
    return bytes.hex(" ").upper()

def generateCRC(fromFile) -> int:
    """Generate bytearray which containts CRC"""

    with open(fromFile, 'rb') as rich:
        richBytes = rich.read()

    tmp = bytearray()
    tmp.extend(bytearray("riCH", "ascii"))
    tmp.extend(richBytes)
    crc = crc32(tmp)
    print(f"Generated CRC from {rich.name} ({stat(rich.name).st_size} bytes) -> {hex(crc)}")
    return crc