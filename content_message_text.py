import telebot
import sqlite3
import re
from const import BASE, REMIND, NOT_UNDERSTAND
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


def athour(message, bot):
    '''
    Принимает сообщения типа:
     В X ТЕКСТ
     В X:Y ТЕКСТ

     Допускаемые символы . : / 
    '''

    try:
        body = re.search(r'(в)\s+(?P<hour>\d{1,2})([.|:|/]?)(?P<minute>\d{0,2})\s*(?P<text>.*)', message.text, re.IGNORECASE)
        
        minute = 0 if body['minute'] == '' else body['minute']
        text = '🤷🏻‍♀️' if body['text'] == '' else body['text']
        

        with sqlite3.connect('base.db') as db:
            cur = db.cursor()
            cur.execute(f"""SELECT timezone FROM {BASE} WHERE chatid = {message.chat.id}""")

            now = datetime.now() + timedelta(hours = cur.fetchone()[0])
            remind_time = datetime(int(now.year), int(now.month), int(now.day), int(body['hour']), int(minute), int(now.second))

            if now > remind_time: # В случае когда пользователь указал час, который уже прошел - переносим на завтра
                remind_time = datetime(int(now.year), int(now.month), int(now.day) + 1, int(body['hour']), int(minute), int(now.second))
                    
            remind = f'{remind_time.strftime("%Y")}.{remind_time.strftime("%m")}.{remind_time.strftime("%d")} {remind_time.strftime("%H")}:{remind_time.strftime("%M")}:{remind_time.strftime("%S")}'
                
            cur.execute(f"""INSERT INTO 'user.{message.chat.id}' VALUES ('{remind}', '{text}')""")

        bot.send_message(message.chat.id, REMIND)
    except:      # На случай если пользователь ввел час > 23 или минуты > 59
        bot.send_message(message.chat.id, NOT_UNDERSTAND)


def inhour(message, bot):
    '''
    Принимает сообщения типа:
     Через X часов ТЕКСТ
    '''

    body = re.search(r'(через)\s+(?P<hour>\d+)\s+(час[ао]?[в]?)\s*(?P<text>.*)', message.text, re.IGNORECASE)       #Получаем тело сообщения

    text = '🤷🏻‍♀️' if body['text'] == '' else body['text']     #Если напоминание пустое, присваиваем эмодзи, чтобы не получить ошибку пустого сообщения при напоминании
    
    with sqlite3.connect('base.db') as db:
        cur = db.cursor()
        cur.execute(f"""SELECT timezone FROM {BASE} WHERE chatid = {message.chat.id}""")

        remind_time = datetime.now() + timedelta(hours=int(body['hour']) + cur.fetchone()[0])
        remind = str(remind_time.strftime("%Y")) + '.' + str(remind_time.strftime("%m")) + '.' + str(remind_time.strftime("%d")) + ' ' + str(remind_time.strftime("%H")) + ':' + str(remind_time.strftime("%M")) + ':' + str(remind_time.strftime("%S"))
               
        cur.execute(f"""INSERT INTO 'user.{message.chat.id}' VALUES ('{remind}', '{text}')""")
        bot.send_message(message.chat.id, REMIND)

def inminute(message, bot):
    '''
    Принимает сообщения типа:
     Через X минут ТЕКСТ
    '''

    body = re.search(r'(через)\s+(?P<minute>\d+)\s+(минут[уы]?)\s*(?P<text>.*)', message.text, re.IGNORECASE)       #Получаем тело сообщения

    text = '🤷🏻‍♀️' if body['text'] == '' else body['text']     #Если напоминание пустое, присваиваем эмодзи, чтобы не получить ошибку пустого сообщения при напоминании
    
    with sqlite3.connect('base.db') as db:
        cur = db.cursor()
        cur.execute(f"""SELECT timezone FROM {BASE} WHERE chatid = {message.chat.id}""")

        remind_time = datetime.now() + timedelta(hours = cur.fetchone()[0], minutes = int(body['minute']))
        remind = str(remind_time.strftime("%Y")) + '.' + str(remind_time.strftime("%m")) + '.' + str(remind_time.strftime("%d")) + ' ' + str(remind_time.strftime("%H")) + ':' + str(remind_time.strftime("%M")) + ':' + str(remind_time.strftime("%S"))

        cur.execute(f"""INSERT INTO 'user.{message.chat.id}' VALUES ('{remind}', '{text}')""")
        bot.send_message(message.chat.id, REMIND)