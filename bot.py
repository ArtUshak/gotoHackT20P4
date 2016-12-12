# -*- coding: utf-8 -*-
import telebot
import mainb
from botlog import *

message_bad_input = "Некорректный запрос. Введите свой логин на Github и язык программирования в формате Логин Язык"
message_can_not_find = "Извините, не можем ничего найти."
message_output = "Больше всего вам подходит: %s"

def get_token():
    token = None
    try:
        with open('../t20p4-token.txt') as token_file:
            token = token_file.readline()
    except FileNotFoundError:
        log('Can not found token file', 'ERROR')
    except BufferError:
        log('Buffer error in token file', 'ERROR')
    except EOFError:
        log('EOF error in token file', 'ERROR')
    return token

token = get_token()

bot = telebot.TeleBot(token)

log('Bot created.')

@bot.message_handler(content_types=["text"])
def process_input(message):
    log(message.text)
    words = message.text.split()
    log(str(words))
    if len(words) != 2:
        bot.send_message(message.chat.id, message_bad_input)
    else:
        name = words[0]
        lang = words[1]
        result = mainb.get_user_matches(name,lang)
        if result == None:
            bot.send_message(message.chat.id, message_can_not_find)
        else:
            bot.send_message(message.chat.id, message_output % result)

if __name__ == '__main__':
    bot.polling(none_stop=True)
