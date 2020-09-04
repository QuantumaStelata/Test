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
    '''
    Принимает сообщения типа:
     %D.$M.%Y в %H.%M ТЕКСТ
     %D.$M.%Y %H.%M ТЕКСТ
     %D.$M.%Y в %H ТЕКСТ
     %D.$M.%Y %H ТЕКСТ

     Допускаемые символы . : / 
    '''

    try:
        body = re.search(r'(?P<day>\d{1,2})[.|:|/](?P<month>\d{1,2})[.|:|/](?P<year>\d{4}|\d{2})\s+(в\s*)?(?P<hour>\d{1,2})[.|:|/]?(?P<minute>\d{0,2})\s*(?P<text>.*)', message.text, re.IGNORECASE)
        
        year = body['year'] if len(body['year']) == 4 else '20' + body['year']
        minute = 0 if body['minute'] == '' else body['minute']
        text = '🤷🏻‍♀️' if body['text'] == '' else body['text']

        now = datetime.now()
        remind_time = datetime(int(year), int(body['month']), int(body['day']), int(body['hour']), int(minute), int(now.second))
        remind = f'{remind_time.strftime("%Y")}.{remind_time.strftime("%m")}.{remind_time.strftime("%d")} {remind_time.strftime("%H")}:{remind_time.strftime("%M")}:{remind_time.strftime("%S")}'

        with sqlite3.connect('base.db') as db:
            cur = db.cursor()  
            cur.execute(f"""INSERT INTO 'user.{message.chat.id}' VALUES ('{remind}', '{text}')""")

        bot.send_message(message.chat.id, REMIND)
    except:        # На случай если пользователь ввел день > 31 или месяц > 12
       bot.send_message(message.chat.id, NOT_UNDERSTAND)
