from io import BytesIO


class GeneralClass:
    """
    Any operation of the BDX file will inherit this class
    """

    def __init__(self) -> None:
        self.operationNumber: int
        self.operationName: str

    def Marshal(self, writer: BytesIO) -> None:
        """
        Marshal GeneralClass into the writer
        """
        ...

    def UnMarshal(self, buffer: BytesIO) -> None:
        """
        Unmarshal the buffer(io object) into GeneralClass
        """
        ...

    def Loads(self, jsonDict: dict) -> None:
        """
        Convert jsonDict:dict into GeneralClass
        """
        ...

    def Dumps(self) -> dict:
        """
        Convert GeneralClass into basic dictionary
        """
        return self.__dict__
