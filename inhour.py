# Принимает сообщения типа:
# Через X часов ТЕКСТ

import telebot
import sqlite3
import re
from const import BASE, REMIND
from datetime import datetime, timedelta

def inhour(message, bot):
    body = re.search(r'(через)\s+(?P<hour>\d+)\s+(час[ао]?[в]?)\s*(?P<text>.*)', message.text, re.IGNORECASE)       #Получаем тело сообщения

    text = '🤷🏻‍♀️' if body['text'] == '' else body['text']     #Если напоминание пустое, присваиваем эмодзи, чтобы не получить ошибку пустого сообщения при напоминании
    
    with sqlite3.connect('base.db') as db:
        cur = db.cursor()
        cur.execute(f"""SELECT timezone FROM {BASE} WHERE chatid = {message.chat.id}""")

        remind_time = datetime.now() + timedelta(hours=int(body['hour']) + cur.fetchone()[0])
        remind = str(remind_time.strftime("%Y")) + '.' + str(remind_time.strftime("%m")) + '.' + str(remind_time.strftime("%d")) + ' ' + str(remind_time.strftime("%H")) + ':' + str(remind_time.strftime("%M")) + ':' + str(remind_time.strftime("%S"))
               
        cur.execute(f"""INSERT INTO 'user.{message.chat.id}' VALUES ('{remind}', '{text}')""")
        bot.send_message(message.chat.id, REMIND)
