# Принимает сообщения типа:
# Через X минут ТЕКСТ

import telebot
import sqlite3
import const
import re
from datetime import datetime, timedelta

def inminute(message):
    minutes = int(re.search(r'\d+', message.text).group())
    text = message.text[re.search(r'\bминут[уы]?', message.text, re.IGNORECASE).end() + 0:].strip().capitalize()

    remind = datetime.now() + timedelta(hours = int(const.copy[str(message.chat.id)]["TZ"]), minutes=minutes)
    remind_text = str(remind.strftime("%Y")) + '.' + str(remind.strftime("%m")) + '.' + str(remind.strftime("%d")) + ' ' + str(remind.strftime("%H")) + ':' + str(remind.strftime("%M")) + ':' + str(remind.strftime("%S"))

    with sqlite3.connect('base.db') as db:
        cur = db.cursor()
        cur.execute(u"""INSERT INTO '{}' VALUES ('{}', '{}')""".format(message.chat.id, remind_text, text))
        const.bot.send_message(message.chat.id, const.remind)


