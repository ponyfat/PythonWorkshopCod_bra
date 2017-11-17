"""
FieldParams class for the /new command of the Miner Telegram bot.
Language: Python 3.2
"""
import exceptions


class FieldParams:
    def __init__(self, message_text):
        splited_message = message_text.split(' ')
        if len(splited_message) != 4 and len(splited_message) != 3:
            raise exceptions.InputErrorException(Exception)
        else:
            try:
                self.width = int(splited_message[1])
            except ValueError:
                raise exceptions.InputErrorException(Exception)
            try:
                self.height = int(splited_message[2])
            except ValueError:
                raise exceptions.InputErrorException(Exception)
            if len(splited_message) == 4:
                try:
                    self.bombs = int(splited_message[3])
                except ValueError:
                    raise exceptions.InputErrorException(Exception)
            else:
                self.bombs = max(1, int(0.25 * self.height * self.width))

        if self.height <= 0 or self.width <= 0:
            raise exceptions.IncorrectParamsException(Exception)
        if self.bombs >= self.width * self.height:
            raise exceptions.TooManyBombsException(Exception)
        if self.height > 15 or self.width > 15:
            raise exceptions.TooLargeFieldException(Exception)
        if self.bombs <= 0:
            raise exceptions.NotEnoughBombsException(Exception)