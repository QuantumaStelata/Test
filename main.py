import telebot
#from telebot import types
from threading import Thread

import re
import json

import const

from reguser import reg
from inminute import inminute
from inhour import inhour
from athour import athour
from atdate import atdate
from delete import delet
from voice import voice
from oldbasedel import old_base_del
from monitoring import monitoring
#import datetime
#from datetime import datetime, timedelta

bot = telebot.TeleBot(const.TOKEN)
const.bot = bot

@bot.message_handler(commands=["start"])
def command_start(message):
    bot.send_message(message.chat.id, const.start, parse_mode="Markdown")

    if str(message.chat.id) not in const.copy.keys():
        msg = bot.send_message(message.chat.id, const.timezonetext, parse_mode="Markdown")
        bot.register_next_step_handler(msg, tz)

def tz(message):
    try:
        timezone = int(message.text)
        if 12 >= timezone and timezone >= -12:
            const.timezone = timezone
            Thread(target=reg, args = (message, )).start()
            bot.send_message(message.chat.id, '✅ Часовой пояс установлен.')
        else:
            msg = bot.send_message(message.chat.id, 'Что-то не так! Попробуйте еще раз ввести свой часовой пояс...')
            bot.register_next_step_handler(msg, tz)
            return
    except:
        msg = bot.send_message(message.chat.id, 'Что-то не так! Попробуйте еще раз ввести свой часовой пояс...')
        bot.register_next_step_handler(msg, tz)


@bot.message_handler(commands=["time"])
def command_time(message):
    msg = bot.send_message(message.chat.id, const.timezonetext)
    bot.register_next_step_handler(msg, changetz)

def changetz(message):
    try:
        timezone = int(message.text)
        if 12 >= timezone >= -12:
            const.timezone = timezone
            const.copy[str(message.chat.id)]["TZ"] = str(const.timezone)
            with open('base.json', 'w', encoding="utf-8") as ff:
                json.dump(const.copy, ff, sort_keys=True, indent=4, ensure_ascii=False)
            bot.send_message(message.chat.id, '✅ Часовой пояс установлен.')
        else:
            msg = bot.send_message(message.chat.id, 'Что-то не так! Попробуйте еще раз...')
            bot.register_next_step_handler(msg, changetz)
    except:
        msg = bot.send_message(message.chat.id, 'Что-то не так! Попробуйте еще раз...')
        bot.register_next_step_handler(msg, changetz)


@bot.message_handler(commands=["callback"])
def command_callback(message):
    msg = bot.send_message(message.chat.id, const.callbacktext, parse_mode="Markdown")
    bot.register_next_step_handler(msg, callback)

def callback(message):
    bot.send_message(403689972, '@' + str(message.from_user.username) + '\nChatId - ' + str(message.chat.id) + '\n\n' + message.text, parse_mode="Markdown")
    bot.send_message(message.chat.id, 'Я отправил, спасибо за обращение 👌', parse_mode="Markdown")


@bot.message_handler(commands=["commands"])
def command_const(message):
    bot.send_message(message.chat.id, const.commands, parse_mode="Markdown")


@bot.message_handler(commands=["list"])
def command_new(message):
    if const.copy[str(message.chat.id)]["Work"] != {}:
        work = '📅 Список твоих дел:\n\n'
        listcopy = sorted(const.copy[str(message.chat.id)]["Work"])

        n = 1
        for j in listcopy:
            work = work + str(n) + ') ' + j.split(' ')[0][8:10] + '.' +j.split(' ')[0][5:7] + '.' +j.split(' ')[0][0:4] + ' в '+ j.split(' ')[1][:-3] + ' - ' + const.copy[str(message.chat.id)]["Work"][j] + '\n'
            n += 1

        work = work + '\nЧтобы удалить пункт напиши - "Удалить (номер пункта)"'
        bot.send_message(message.chat.id, work, parse_mode="Markdown")

        const.copy[str(message.chat.id)]["List"] = str(message.message_id)
        Thread(target=const.save).start()

    else:
        bot.send_message(message.chat.id, 'У тебя нет дел 😔', parse_mode="Markdown")

@bot.message_handler(content_types=["sticker"])
def mainsticker(message):
    file_info = bot.get_file(message.sticker.file_id)
    bot.send_sticker(message.chat.id, 'CAACAgUAAxkBAAIBtF8W4mnS44I1futOLOabjzGI5BuJAAL_AANxffwUdic7ErtbrcEaBA')

@bot.message_handler(content_types=["voice"])
def mainvoice(message):
    voice(message)
    main(message)

@bot.message_handler(content_types=["text"])
def main(message):
    print(message.text)
    
    if re.search(r'(\d{1,2}[.|:|/]{1}\d{1,2}[.|:|/]{1}\d{2,4})(\s*)([в]\s*)?(\d{1,2}[.|:|/]{0,1}\d{0,2})', message.text, re.IGNORECASE):
        Thread(target=atdate, args=(message,)).start()
    
    elif re.search(r'[в]{1}\s*(\d{1,2}[.|:|/]{0,1}\d{0,2})', message.text, re.IGNORECASE):
        Thread(target=athour, args=(message,)).start()

    elif re.search(r'\bчерез\b', message.text, re.IGNORECASE):
        if re.search(r'\bминут[уы]?', message.text, re.IGNORECASE):
            if re.search(r'\bчерез\b \d+ \bминут[уы]?', message.text, re.IGNORECASE):
                Thread(target=inminute, args=(message,)).start()
            else:
                bot.send_message(message.chat.id, const.not_understand)

        elif re.search(r'\bчас[ао]*[в]?', message.text, re.IGNORECASE):
            if re.search(r'\bчерез\b \d+ \bчас[ао]*[в]?', message.text, re.IGNORECASE):
                Thread(target=inhour, args=(message,)).start()
            else:
                bot.send_message(message.chat.id, const.not_understand)
        else:
            bot.send_message(message.chat.id, const.not_understand)

    elif re.search(r'удалить.?\d+', message.text, re.IGNORECASE):
        Thread(target=delet, args=(message.chat.id, message)).start()

    else:
        bot.send_message(message.chat.id, const.not_understand)




'''keyboard = types.InlineKeyboardMarkup()
    key_oven = types.InlineKeyboardButton(text='Овен', callback_data='test')
    keyboard.add(key_oven)
    bot.send_message(message.chat.id, "Нажми лучше на одну из кнопок ниже ⬇️", reply_markup=keyboard)'''
'''@ bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    if call.data == "test":
        bot.send_message(call.message.chat.id, 'текст')'''


if __name__ == '__main__':
    const.push()                        # Рассылка по всем пользователям
    old_base_del()                      # Удаление старых записей
    Thread(target=monitoring).start()   # Запуск 2-ого потока - функция monitoring из monitoring.py
    bot.infinity_polling()
