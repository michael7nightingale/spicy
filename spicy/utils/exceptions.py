class SpicyException(Exception):
    """Base spicy exception"""
    def __init__(self, message=None):
        if message is None:
            message = self.__doc__
        super().__init__(message)


class DoctypeException(SpicyException):
    """Invalid doctype: _. """
    def __init__(self, message = None, doctype: str = None):
        if message is None:
            message = self.__doc__
        if doctype is not None:
            message = message.replace('_', doctype)
        super().__init__(message)


class TreeError(SpicyException):
    """Error while building tree"""




