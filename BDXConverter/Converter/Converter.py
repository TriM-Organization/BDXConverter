from ..General.GeneralClass import GeneralClass
from ..General.Pool import GetBDXCommandPool
from ..utils.getString import getByte, getString
from .Signature import Signature
from .ErrorClassDefine import headerError
from .ErrorClassDefine import readError, unknownOperationError
from brotli import compress, decompress
from io import BytesIO
from copy import deepcopy


class BDX(GeneralClass):
    def __init__(self) -> None:
        """
        `AuthorName: str`
            The author of this BDX file
                Note: The default value is "TriM-Organization/BDXConverter"
        `BDXContent: list[GeneralClass]`
            The valid contents of the BDX file
        `Signature: Signature`
            The signature data of the BDX file
        """
        self.AuthorName: str = 'TriM-Organization/BDXConverter'
        self.BDXContent: list[GeneralClass] = []
        self.Signature: Signature = Signature()

    def Marshal(self, writer: BytesIO) -> None:
        newWriter = BytesIO(
            b'BDX\x00'+self.AuthorName.encode(encoding='utf-8')+b'\x00')
        newWriter.seek(0, 2)
        # inside header with author's name
        for i in self.BDXContent:
            newWriter.write(i.operationNumber.to_bytes(
                length=1, byteorder='big', signed=False))
            i.Marshal(newWriter)
        # valid contents
        if self.Signature.signedOrNeedToSign == True and self.Signature.isLegacy == False:
            self.Signature.BDXContentWithInsideHeader = newWriter
            self.Signature.Marshal(newWriter)
        else:
            newWriter.write(b'XE')
        # signature
        writer.write(b'BD@'+compress(newWriter.getvalue()))
        # write BDX datas

    def UnMarshal(self, binaryDatas: bytes) -> None:
        if binaryDatas[0:3] != b'BD@':
            raise headerError(binaryDatas[:3])
        # check outside header
        reader = BytesIO(decompress(binaryDatas[3:]))
        # get reader to read valid contents
        insideHeader = getByte(reader, 3)
        if insideHeader != b'BDX':
            raise headerError(insideHeader)
        # check inside header
        firstOperation = getByte(reader, 1)
        if firstOperation != b'\x00':
            raise unknownOperationError(firstOperation[0], reader.seek(-1, 1))
        self.AuthorName = getString(reader)
        # get author's name
        BDXCommandPool: dict[int, GeneralClass] = GetBDXCommandPool()
        # get bdx command(operation) pool
        while True:
            commandId = getByte(reader, 1)[0]
            if commandId == 88:
                break
            elif commandId in BDXCommandPool:
                struct: GeneralClass = deepcopy(BDXCommandPool[commandId])
                # get struct(operation) from the pool
                errorType = 0
                # prepare
                try:
                    struct.UnMarshal(reader)
                except EOFError:
                    errorType = 1
                except:
                    errorType = 2
                # unmarshal bytes into the struct
                if errorType == 1:
                    raise EOFError
                elif errorType == 2:
                    raise readError(reader.seek(0, 1))
                # if meet error
                self.BDXContent.append(struct)
                # submit single datas
        # read datas from reader
        self.Signature.UnMarshal(reader)
        if self.Signature.isLegacy == False and self.Signature.signedOrNeedToSign == True:
            reader.truncate(reader.seek(-1, 1))
            self.Signature.BDXContentWithInsideHeader = reader
            self.Signature.verifySignature()
        # signature

    def Loads(self, jsonDict: dict) -> None:
        BDXCommandPool: dict[int, GeneralClass] = GetBDXCommandPool()

        self.AuthorName = jsonDict['AuthorName'] if 'AuthorName' in jsonDict else ''
        if 'Signature' in jsonDict:
            self.Signature.Loads(jsonDict['Signature'])
        if 'BDXContent' in jsonDict:
            tmp: list[dict] = jsonDict['BDXContent']
            for i in tmp:
                if not 'operationNumber' in i:
                    continue
                if not 'operationDatas' in i:
                    continue
                commandId: int = i['operationNumber']
                struct: GeneralClass = deepcopy(BDXCommandPool[commandId])
                struct.Loads(i['operationDatas'])
                self.BDXContent.append(struct)

    def Dumps(self) -> dict:
        return {
            'AuthorName': self.AuthorName,
            'BDXContent': [i.Dumps() for i in self.BDXContent],
            'Signature': self.Signature.Dumps()
        }
