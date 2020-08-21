# Принимает сообщения типа:
# Через X минут ТЕКСТ

import telebot
import sqlite3
import re
from const import BASE, REMIND
from datetime import datetime, timedelta

def inminute(message, bot):
    body = re.search(r'(через)\s+(?P<minute>\d+)\s+(минут[уы]?)\s*(?P<text>.*)', message.text, re.IGNORECASE)       #Получаем тело сообщения

    text = '🤷🏻‍♀️' if body['text'] == '' else body['text']     #Если напоминание пустое, присваиваем эмодзи, чтобы не получить ошибку пустого сообщения при напоминании
    
    with sqlite3.connect('base.db') as db:
        cur = db.cursor()
        cur.execute(u"""SELECT timezone FROM {} WHERE chatid = {}""".format(BASE, message.chat.id))

        remind_time = datetime.now() + timedelta(hours = cur.fetchone()[0], minutes = int(body['minute']))
        remind = str(remind_time.strftime("%Y")) + '.' + str(remind_time.strftime("%m")) + '.' + str(remind_time.strftime("%d")) + ' ' + str(remind_time.strftime("%H")) + ':' + str(remind_time.strftime("%M")) + ':' + str(remind_time.strftime("%S"))

        cur.execute(u"""INSERT INTO '{}' VALUES ('{}', '{}')""".format(message.chat.id, remind, text))
        bot.send_message(message.chat.id, REMIND)


