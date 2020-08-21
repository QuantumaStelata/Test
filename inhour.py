# Принимает сообщения типа:
# Через X часов ТЕКСТ

import telebot
import sqlite3
import re
from const import base, remind
from datetime import datetime, timedelta


def inhour(message, bot):
    hours = int(re.search(r'\d+', message.text).group())
    text = message.text[re.search(r'\bчас[ао]*[в]?', message.text, re.IGNORECASE).end() + 0:].strip().capitalize()
                
    with sqlite3.connect('base.db') as db:
        cur = db.cursor()
        cur.execute(u"""SELECT timezone FROM {} WHERE chatid = {}""".format(base, message.chat.id))

        remind_ = datetime.now() + timedelta(hours=hours + cur.fetchone()[0])
        remind_text = str(remind_.strftime("%Y")) + '.' + str(remind_.strftime("%m")) + '.' + str(remind_.strftime("%d")) + ' ' + str(remind_.strftime("%H")) + ':' + str(remind_.strftime("%M")) + ':' + str(remind_.strftime("%S"))
               
        cur.execute(u"""INSERT INTO '{}' VALUES ('{}', '{}')""".format(message.chat.id, remind_text, text))
        bot.send_message(message.chat.id, remind)
