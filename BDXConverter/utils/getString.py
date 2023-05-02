from io import BytesIO
from .getByte import getByte


def getString(buffer: BytesIO) -> str:
    writer = BytesIO(b'')
    while True:
        currentByte = getByte(buffer, 1)
        if currentByte == b'\x00':
            return writer.getvalue().decode(encoding='utf-8')
        else:
            writer.write(currentByte)
