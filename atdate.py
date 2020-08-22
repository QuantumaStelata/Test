# Принимает сообщения типа:
# %D.$M.%Y в %H.%M ТЕКСТ
# %D.$M.%Y %H.%M ТЕКСТ
# %D.$M.%Y в %H ТЕКСТ
# %D.$M.%Y %H ТЕКСТ

# Допускаемые символы . : / 

import telebot
import sqlite3
import re
from const import REMIND, NOT_UNDERSTAND
from datetime import datetime, timedelta

def atdate(message, bot):
    try:
        body = re.search(r'(?P<day>\d{1,2})[.|:|/](?P<month>\d{1,2})[.|:|/](?P<year>\d{4}|\d{2})\s+(в\s*)?(?P<hour>\d{1,2})[.|:|/]?(?P<minute>\d{0,2})\s*(?P<text>.*)', message.text, re.IGNORECASE)
        
        year = body['year'] if len(body['year']) == 4 else '20' + body['year']
        minute = 0 if body['minute'] == '' else body['minute']
        text = '🤷🏻‍♀️' if body['text'] == '' else body['text']

        now = datetime.now()
        remind_time = datetime(int(year), int(body['month']), int(body['day']), int(body['hour']), int(minute), int(now.second))
        remind = str(remind_time.strftime("%Y")) + '.' + str(remind_time.strftime("%m")) + '.' + str(remind_time.strftime("%d")) + ' ' + str(remind_time.strftime("%H")) + ':' + str(remind_time.strftime("%M")) + ':' + str(remind_time.strftime("%S"))

        with sqlite3.connect('base.db') as db:
            cur = db.cursor()  
            cur.execute(u"""INSERT INTO '{}' VALUES ('{}', '{}')""".format(message.chat.id, remind, text))

        bot.send_message(message.chat.id, REMIND)
    except:        # На случай если пользователь ввел день > 31 или месяц > 12
       bot.send_message(message.chat.id, NOT_UNDERSTAND)
