from ..General.GeneralClass import GeneralClass


class NOP(GeneralClass):
    def __init__(self) -> None:
        self.operationName: str = 'NOP'
        self.operationNumber: int = 9
