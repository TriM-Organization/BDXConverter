class notAcorrectBDXFileError(Exception):
    """
    Not a correct BDX file error
    """

    def __init__(self, path: str):
        Exception.__init__(self, f'"{path}" is not a correct BDX file')


class readError(Exception):
    """
    BDX file read error
    """

    def __init__(self, errorOccurredPosition: int):
        Exception.__init__(
            self, f'failed to convert this BDX file, and the error occurred at position {errorOccurredPosition}')


class unknownOperationError(Exception):
    """
    Find unknown operation error
    """

    def __init__(self, operationId: int, errorOccurredPosition: int):
        Exception.__init__(
            self, f'an unknown operation {operationId} was found, and the error occurred at position {errorOccurredPosition}')
