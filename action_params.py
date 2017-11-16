import exceptions


class ActionParams:
    def __init__(self, message_text, field_height, field_width):
        splited_message = message_text.split(' ')
        if len(splited_message) != 3:
            raise exceptions.InputErrorException(Exception)
        else:
            try:
                self.x = int(splited_message[1]) - 1
            except ValueError:
                raise exceptions.InputErrorException(Exception)
            try:
                self.y = int(splited_message[2]) - 1
            except ValueError:
                raise InputErrorException(Exception)
        if self.x < 0 or self.x >= field_height:
            raise exceptions.IncorrectParamsException(Exception)
        if self.y < 0 or self.y >= field_width:
            raise exceptions.IncorrectParamsException(Exception)