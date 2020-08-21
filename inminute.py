# Принимает сообщения типа:
# Через X минут ТЕКСТ

import telebot
import sqlite3
import re
from const import base, remind
from datetime import datetime, timedelta

def inminute(message, bot):
    minutes = int(re.search(r'\d+', message.text).group())
    text = message.text[re.search(r'\bминут[уы]?', message.text, re.IGNORECASE).end() + 0:].strip().capitalize()

    with sqlite3.connect('base.db') as db:
        cur = db.cursor()
        cur.execute(u"""SELECT timezone FROM {} WHERE chatid = {}""".format(base, message.chat.id))

        remind_ = datetime.now() + timedelta(hours = cur.fetchone()[0], minutes=minutes)
        remind_text = str(remind_.strftime("%Y")) + '.' + str(remind_.strftime("%m")) + '.' + str(remind_.strftime("%d")) + ' ' + str(remind_.strftime("%H")) + ':' + str(remind_.strftime("%M")) + ':' + str(remind_.strftime("%S"))

        cur.execute(u"""INSERT INTO '{}' VALUES ('{}', '{}')""".format(message.chat.id, remind_text, text))
        bot.send_message(message.chat.id, remind)


