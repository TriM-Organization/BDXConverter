from io import BytesIO
from copy import deepcopy


class GeneralClass:
    """
    Any operation of the BDX file will inherit this class
    """

    def __init__(self) -> None:
        self.operationNumber: int
        self.operationName: str

    def Marshal(self, writer: BytesIO) -> None:
        """
        Marshal Self@GeneralClass into the writer(io object)
        """
        ...

    def UnMarshal(self, buffer: BytesIO) -> None:
        """
        Unmarshal the buffer(io object) into Self@GeneralClass
        """
        ...

    def Loads(self, jsonDict: dict) -> None:
        """
        Load datas from jsonDict:dict
        """
        if 'operationNumber' in self.__dict__:
            jsonDict['operationNumber'] = self.operationNumber
            jsonDict['operationName'] = self.operationName
        if 'operationDatas' in self.__dict__:
            for i in self.__dict__['operationDatas']:
                if i in jsonDict:
                    self.__dict__['operationDatas'][i] = jsonDict[i]
        else:
            for i in self.__dict__:
                if i in jsonDict:
                    self.__dict__[i] = jsonDict[i]

    def Dumps(self) -> dict:
        """
        Convert Self@GeneralClass into the basic dictionary
        """
        if 'operationNumber' in self.__dict__:
            copyDict = deepcopy(self.__dict__)
            del copyDict['operationNumber']
            del copyDict['operationName']
            return {
                'operationNumber': self.operationNumber,
                'operationName': self.operationName,
                'operationDatas': copyDict
            }
        else:
            return self.__dict__
