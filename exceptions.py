"""
Exceptions for the Miner Telegram bot implementation.
Language: Python 3.2
"""
class InputErrorException(Exception):
    pass


class IncorrectParamsException(Exception):
    pass


class TooLargeField(Exception):
    pass


class TooManyBombsException(Exception):
    pass


class NotEnoughBombsException(Exception):
    pass


class TooLargeFieldException(Exception):
    pass