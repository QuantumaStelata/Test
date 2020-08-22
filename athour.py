# Принимает сообщения типа:
# В X ТЕКСТ
# В X:Y ТЕКСТ

# Допускаемые символы . : / 

import telebot
import sqlite3
import re
from const import BASE, REMIND, NOT_UNDERSTAND
from datetime import datetime, timedelta

def athour(message, bot):
    try:
        body = re.search(r'(в)\s+(?P<hour>\d{1,2})([.|:|/]?)(?P<minute>\d{0,2})\s*(?P<text>.*)', message.text, re.IGNORECASE)
        
        minute = 0 if body['minute'] == '' else body['minute']
        text = '🤷🏻‍♀️' if body['text'] == '' else body['text']
        

        with sqlite3.connect('base.db') as db:
            cur = db.cursor()
            cur.execute(u"""SELECT timezone FROM {} WHERE chatid = {}""".format(BASE, message.chat.id))

            now = datetime.now() + timedelta(hours = cur.fetchone()[0])
            remind_time = datetime(int(now.year), int(now.month), int(now.day), int(body['hour']), int(minute), int(now.second))

            if now > remind_time: # В случае когда пользователь указал час, который уже прошел - переносим на завтра
                remind_time = datetime(int(now.year), int(now.month), int(now.day) + 1, int(body['hour']), int(minute), int(now.second))
                    
            remind = str(remind_time.strftime("%Y")) + '.' + str(remind_time.strftime("%m")) + '.' + str(remind_time.strftime("%d")) + ' ' + str(remind_time.strftime("%H")) + ':' + str(remind_time.strftime("%M")) + ':' + str(remind_time.strftime("%S"))
                
            cur.execute(u"""INSERT INTO '{}' VALUES ('{}', '{}')""".format(message.chat.id, remind, text))

        bot.send_message(message.chat.id, REMIND)
    except:      # На случай если пользователь ввел час > 23 или минуты > 59
        bot.send_message(message.chat.id, NOT_UNDERSTAND)

        