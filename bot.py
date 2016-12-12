# -*- coding: utf-8 -*-
import config
import telebot
import mainb
bot = telebot.TeleBot(config.token)


@bot.message_handler(content_types=["text"])
def repeat_all_messages(message):
    print(message.text)
    a = message.text.split()
    print(a)
    name = a[0]
    lang = a[1]
    ar = mainb.get_user_mathes(name,lang)
    bot.send_message(message.chat.id, "Больше всего вам подходит:  "+ar)




if __name__ == '__main__':
    bot.polling(none_stop=True)
