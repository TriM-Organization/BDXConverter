from io import BytesIO
from ..General.GeneralClass import GeneralClass
from ..utils.getString import getString


class CreateConstantString(GeneralClass):
    def __init__(self) -> None:
        self.operationName: str = 'CreateConstantString'
        self.operationNumber: int = 1
        self.constantString: str = ''

    def Marshal(self, writer: BytesIO) -> None:
        writer.write(self.constantString.encode(encoding='utf-8') + b'\x00')

    def UnMarshal(self, buffer: BytesIO) -> None:
        self.constantString = getString(buffer)

    def Loads(self, jsonDict: dict) -> None:
        self.constantString = jsonDict['constantString'] if 'constantString' in jsonDict else ''
