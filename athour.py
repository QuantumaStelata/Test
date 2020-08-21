# Принимает сообщения типа:
# В X ТЕКСТ
# В X:Y ТЕКСТ

import telebot
import sqlite3
import re
from const import BASE, REMIND, NOT_UNDERSTAND
from oldbasedel import old_base_del
from datetime import datetime, timedelta
from threading import Thread

def athour(message, bot):
    try:
        hour_minute = re.findall(r'(\d{1,2}[.|:|/]{0,1}\d{0,2})', message.text)[0]
        hour_minute = re.split(r'[.|:|/]', hour_minute)     # Получаем список [час, минут]

        hour = hour_minute[0]   # Час

        try: # Проверяем написал ли пользователь минуты
            minute = hour_minute[1] if hour_minute[1] != '' else 0      # Минуты
        except:
            minute = 0      # Минуты
                
        text = message.text[re.search(r'(\d{1,2}[.|:|/]{0,1}\d{0,2})', message.text, re.IGNORECASE).end() + 0:].strip().capitalize() 
            
        
        with sqlite3.connect('base.db') as db:
            cur = db.cursor()
            cur.execute(u"""SELECT timezone FROM {} WHERE chatid = {}""".format(BASE, message.chat.id))

            now = datetime.now() + timedelta(hours = cur.fetchone()[0])
            remind_ = datetime(int(now.year), int(now.month), int(now.day), int(hour), int(minute), int(now.second))

            if now > remind_: # В случае когда пользователь указал час, который уже прошел - переносим на завтра
                remind_ = datetime(int(now.year), int(now.month), int(now.day) + 1, int(hour), int(minute), int(now.second))
                
            remind_text = str(remind_.strftime("%Y")) + '.' + str(remind_.strftime("%m")) + '.' + str(remind_.strftime("%d")) + ' ' + str(remind_.strftime("%H")) + ':' + str(remind_.strftime("%M")) + ':' + str(remind_.strftime("%S"))
            
            cur.execute(u"""INSERT INTO '{}' VALUES ('{}', '{}')""".format(message.chat.id, remind_text, text))

        bot.send_message(message.chat.id, REMIND)


    except:
        bot.send_message(message.chat.id, NOT_UNDERSTAND)
        