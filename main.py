import telebot
from threading import Thread

import re
import sqlite3

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


bot = telebot.TeleBot(const.TOKEN)
const.bot = bot


@bot.message_handler(commands=["start"])
def command_start(message):
    bot.send_message(message.chat.id, const.start, parse_mode="Markdown")

    with sqlite3.connect('base.db') as db:
        cur = db.cursor()

        cur.execute(u"""SELECT chatid FROM {}""".format(const.base))
        chatid = [i[0] for i in cur.fetchall()]

        if message.chat.id not in chatid:
            msg = bot.send_message(message.chat.id, const.timezonetext, parse_mode="Markdown")
            bot.register_next_step_handler(msg, tz)
        

def tz(message):
    try:
        timezone = int(message.text)
        if 12 >= timezone and timezone >= -12:
            Thread(target=reg, args = (message, timezone)).start()
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
            with sqlite3.connect('base.db') as db:
                db.cursor().execute(u"""UPDATE {} SET timezone = {} WHERE chatid = {}""".format(const.base, timezone, message.chat.id))
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
    with sqlite3.connect('base.db') as db:
        cur = db.cursor()

        cur.execute(u"""SELECT * FROM '{}'""".format(message.chat.id))

        if cur.fetchall() != []:
            cur.execute(u"""SELECT * FROM '{}' ORDER BY time""".format(message.chat.id))
        
            work = '📅 Список твоих дел:\n\n'
            

            n = 1
            for i in cur.fetchall():
                work = work + str(n) + ') ' + i[0].split(' ')[0][8:10] + '.' + i[0].split(' ')[0][5:7] + '.' + i[0].split(' ')[0][0:4] + ' в '+ i[0].split(' ')[1][:-3] + ' - ' + i[1] + '\n'
                n += 1

            work = work + '\nЧтобы удалить пункт напиши - "Удалить (номер пункта)"'
            bot.send_message(message.chat.id, work, parse_mode="Markdown")
            cur.execute(u"""UPDATE '{}' SET listid = {} WHERE chatid = {}""".format(const.base, message.message_id + 1, message.chat.id))

        else:
            bot.send_message(message.chat.id, 'У тебя нет дел 😔', parse_mode="Markdown")

@bot.message_handler(content_types=["sticker"])
def mainsticker(message):
    file_info = bot.get_file(message.sticker.file_id)
    bot.send_sticker(message.chat.id, 'CAACAgUAAxkBAAIBtF8W4mnS44I1futOLOabjzGI5BuJAAL_AANxffwUdic7ErtbrcEaBA')

@bot.message_handler(content_types=["voice"])
def mainvoice(message):
    voice(message, bot)
    main(message)

@bot.message_handler(content_types=["text"])
def main(message):
    print(message.text)
    
    if re.search(r'(\d{1,2}[.|:|/]{1}\d{1,2}[.|:|/]{1}\d{2,4})(\s*)([в]\s*)?(\d{1,2}[.|:|/]{0,1}\d{0,2})', message.text, re.IGNORECASE):
        Thread(target=atdate, args=(message, bot)).start()
    
    elif re.search(r'[в]{1}\s*(\d{1,2}[.|:|/]{0,1}\d{0,2})', message.text, re.IGNORECASE):
        Thread(target=athour, args=(message, bot)).start()

    elif re.search(r'\bчерез\b', message.text, re.IGNORECASE):
        if re.search(r'\bминут[уы]?', message.text, re.IGNORECASE):
            if re.search(r'\bчерез\b \d+ \bминут[уы]?', message.text, re.IGNORECASE):
                Thread(target=inminute, args=(message, bot)).start()
            else:
                bot.send_message(message.chat.id, const.not_understand)

        elif re.search(r'\bчас[ао]*[в]?', message.text, re.IGNORECASE):
            if re.search(r'\bчерез\b \d+ \bчас[ао]*[в]?', message.text, re.IGNORECASE):
                Thread(target=inhour, args=(message, bot)).start()
            else:
                bot.send_message(message.chat.id, const.not_understand)
        else:
            if message.chat.id > 0:
                bot.send_message(message.chat.id, const.not_understand)

    elif re.search(r'удалить.?\d+', message.text, re.IGNORECASE):
        Thread(target=delet, args=(message, bot)).start()

    else:
        if message.chat.id > 0:
            bot.send_message(message.chat.id, const.not_understand)


if __name__ == '__main__':
    const.push()                        # Рассылка по всем пользователям
    old_base_del()                      # Удаление старых записей
    Thread(target=monitoring, args=(bot,)).start()   # Запуск 2-ого потока - функция monitoring из monitoring.py
    bot.infinity_polling()
