import telebot
import os
import config
import exceptions
import constants

from action_params import ActionParams
from field_params import FieldParams
from gamefield import GameField

bot = telebot.TeleBot(config.token)
users = {}


def registration_check(message):
    if message.chat.id not in users.keys():
        bot.send_message(message.chat.id, 'Начните новую игру')
        return False
    if not users[message.chat.id].playing:
        bot.send_message(message.chat.id, 'Начните новую игру')
        return False
    return True


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_sticker(message.chat.id, data='CAADAgADCBMAAkKvaQABJS_tlanrZB8C')
    bot.send_message(message.chat.id, constants.HELP_MESSAGE)
    users[message.chat.id] = GameField()


@bot.message_handler(commands=['new'])
def new_game_check(message):
    if message.chat.id not in users.keys():
        users[message.chat.id] = GameField()
    try:
        user_arguments = FieldParams(message.text)
    except exceptions.InputErrorException:
        bot.send_message(message.chat.id, 'Ошибка ввода')
        return
    except exceptions.TooManyBombsException:
        bot.send_message(message.chat.id, "Слишком много бомб")
        return
    except exceptions.TooLargeFieldException:
        bot.send_message(message.chat.id, "Слишком большое поле : размеры должны быть меньше 16")
        return
    except exceptions.IncorrectParamsException:
        bot.send_message(message.chat.id, "Некорректный размер поля")
        return
    except exceptions.NotEnoughBombsException:
        bot.send_message(message.chat.id, "Маловато бомб")
        return
    if user_arguments.bombs % 10 == 1 and user_arguments.bombs != 11:
        bot.send_message(message.chat.id, 'На поле {} бомба'.format(user_arguments.bombs))
    elif 2 <= user_arguments.bombs % 10 <= 4 and (user_arguments.bombs <= 10 or user_arguments.bombs >= 20):
        bot.send_message(message.chat.id, 'Ha поле {} бомбы'.format(user_arguments.bombs))
    else:
        bot.send_message(message.chat.id, 'Ha поле {} бомб'.format(user_arguments.bombs))
    users[message.chat.id].init_game_field(user_arguments, message.chat.id)
    with open('/'.join([os.getcwd(), 'users/{}.jpg'.format(message.chat.id)]), 'rb') as photo:
        bot.send_photo(message.chat.id, photo)


@bot.message_handler(commands=['open'])
def open_cell_check(message):
    if not registration_check(message):
        return
    try:
        open_params = ActionParams(message.text,
                                   field_height=users[message.chat.id].height,
                                   field_width=users[message.chat.id].width)
    except (exceptions.InputErrorException, exceptions.IncorrectParamsException):
        bot.send_message(message.chat.id, 'Ошибка ввода')
        return
    if users[message.chat.id].user_field[open_params.x][open_params.y] not in [constants.EMPTY, constants.FLAGGED]:
        bot.send_message(message.chat.id, 'Ячейка уже открыта')
    else:
        open_cell(message.chat.id, open_params.x, open_params.y)


def open_cell(chat_id, x, y):
    result = users[chat_id].open_cell(x, y)
    with open('/'.join([os.getcwd(), 'users/{}.jpg'.format(chat_id)]), 'rb') as photo:
        if result == constants.LOSER:
            bot.send_message(chat_id, 'Бууум! Ты проиграл!')
            bot.send_photo(chat_id, photo)
            bot.send_sticker(chat_id, data='CAADAgAD7wADcqrmBE6HbRTJbkh-Ag')
            return
        elif result == constants.WINNER:
            bot.send_message(chat_id, 'С победой!')
            bot.send_photo(chat_id, photo)
            bot.send_sticker(chat_id, data='CAADAgADBwQAAnKq5gTVZI_e9jff8wI')
            return
        bot.send_photo(chat_id, photo)


@bot.message_handler(commands=['flag'])
def flag_cell(message):
    if not registration_check(message):
        return
    try:
        flag_params = ActionParams(message.text,
                                   field_height=users[message.chat.id].height,
                                   field_width=users[message.chat.id].width)
    except (exceptions.IncorrectParamsException, exceptions.InputErrorException):
        bot.send_message(message.chat.id, 'Ошибка ввода')
        return
    if users[message.chat.id].user_field[flag_params.x][flag_params.y] != constants.EMPTY:
        bot.send_message(message.chat.id, "Ячейка уже открыта")
        return
    if not users[message.chat.id].flag_cell(flag_params.x, flag_params.y):
        bot.send_message(message.chat.id, 'В этой ячейке уже есть флажок')
    else:
        with open('/'.join([os.getcwd(), 'users/{}.jpg'.format(message.chat.id)]), 'rb') as photo:
            bot.send_photo(message.chat.id, photo)


@bot.message_handler(commands=['remove_flag'])
def remove_flag_cell(message):
    if not registration_check(message):
        return
    try:
        remove_params = ActionParams(message.text,
                                     field_height=users[message.chat.id].height,
                                     field_width=users[message.chat.id].width)
    except (exceptions.InputErrorExceptionm, exceptions.IncorrectParamsException):
        bot.send_message(message.chat.id, 'Ошибка ввода')
        return
    if not users[message.chat.id].remove_flag_cell(remove_params.x, remove_params.y):
        bot.send_message(message.chat.id, 'В этой ячейке нет флажка')
        return
    with open('/'.join([os.getcwd(), 'users/{}.jpg'.format(message.chat.id)]), 'rb') as photo:
        bot.send_photo(message.chat.id, photo)


@bot.message_handler(commands=['help'])
def help_(message):
    bot.send_message(message.chat.id, constants.HELP_MESSAGE)


@bot.message_handler()
def wrong_command(message):
    bot.send_message(message.chat.id, 'Ошибка ввода')


if __name__ == '__main__':
    bot.polling(none_stop=False)
