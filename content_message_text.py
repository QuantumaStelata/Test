import telebot
import sqlite3
import re
from const import BASE, TABLE, REMIND, NOT_UNDERSTAND
from datetime import datetime, timedelta
from log.logger import *


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

        with sqlite3.connect(BASE) as db:
            cur = db.cursor()  
            cur.execute(f"""INSERT INTO 'user.{message.chat.id}' VALUES ('{remind}', '{text}')""")

        bot.send_message(message.chat.id, REMIND)
    except:        # На случай если пользователь ввел день > 31 или месяц > 12
       bot.send_message(message.chat.id, NOT_UNDERSTAND)


def athour(message, bot):
    '''
    Принимает сообщения типа:
     В %H ТЕКСТ
     В %H.%M ТЕКСТ

     Допускаемые символы . : / 
    '''

    try:
        body = re.search(r'(в)\s+(?P<hour>\d{1,2})([.|:|/]?)(?P<minute>\d{0,2})\s*(?P<text>.*)', message.text, re.IGNORECASE)
        
        minute = 0 if body['minute'] == '' else body['minute']
        text = '🤷🏻‍♀️' if body['text'] == '' else body['text']
        

        with sqlite3.connect(BASE) as db:
            cur = db.cursor()
            cur.execute(f"""SELECT timezone FROM {TABLE} WHERE chatid = {message.chat.id}""")

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
     Через %H часов ТЕКСТ
    '''

    body = re.search(r'(через)\s+(?P<hour>\d+)\s+(час[ао]?[в]?)\s*(?P<text>.*)', message.text, re.IGNORECASE)       #Получаем тело сообщения

    text = '🤷🏻‍♀️' if body['text'] == '' else body['text']     #Если напоминание пустое, присваиваем эмодзи, чтобы не получить ошибку пустого сообщения при напоминании
    
    with sqlite3.connect(BASE) as db:
        cur = db.cursor()
        cur.execute(f"""SELECT timezone FROM {TABLE} WHERE chatid = {message.chat.id}""")

        remind_time = datetime.now() + timedelta(hours=int(body['hour']) + cur.fetchone()[0])
        remind = str(remind_time.strftime("%Y")) + '.' + str(remind_time.strftime("%m")) + '.' + str(remind_time.strftime("%d")) + ' ' + str(remind_time.strftime("%H")) + ':' + str(remind_time.strftime("%M")) + ':' + str(remind_time.strftime("%S"))
               
        cur.execute(f"""INSERT INTO 'user.{message.chat.id}' VALUES ('{remind}', '{text}')""")
        bot.send_message(message.chat.id, REMIND)


def inminute(message, bot):
    '''
    Принимает сообщения типа:
     Через %M минут ТЕКСТ
    '''

    body = re.search(r'(через)\s+(?P<minute>\d+)\s+(минут[уы]?)\s*(?P<text>.*)', message.text, re.IGNORECASE)       #Получаем тело сообщения

    text = '🤷🏻‍♀️' if body['text'] == '' else body['text']     #Если напоминание пустое, присваиваем эмодзи, чтобы не получить ошибку пустого сообщения при напоминании
    
    with sqlite3.connect(BASE) as db:
        cur = db.cursor()
        cur.execute(f"""SELECT timezone FROM {TABLE} WHERE chatid = {message.chat.id}""")

        remind_time = datetime.now() + timedelta(hours = cur.fetchone()[0], minutes = int(body['minute']))
        remind = str(remind_time.strftime("%Y")) + '.' + str(remind_time.strftime("%m")) + '.' + str(remind_time.strftime("%d")) + ' ' + str(remind_time.strftime("%H")) + ':' + str(remind_time.strftime("%M")) + ':' + str(remind_time.strftime("%S"))

        cur.execute(f"""INSERT INTO 'user.{message.chat.id}' VALUES ('{remind}', '{text}')""")
        bot.send_message(message.chat.id, REMIND)


def delet(message, bot):
    '''
    Функция для удаления определенных записей, которые выберет пользователь
     Так же редактирует последний вызванный /list после удаления записи
    '''
    
    index = int(re.search(r'\d+', message.text).group())

    with sqlite3.connect(BASE) as db:
        cur = db.cursor()
        cur.execute(f"""SELECT * FROM 'user.{message.chat.id}' ORDER BY time""")
        body = [i for i in cur.fetchall()]      # Получаем список записок пользователя
        
        if body == []:      # Если у пользователя нет записи, выходим из функции
            bot.send_message(message.chat.id, 'У тебя нет дел 😔')
            return
        
        if index <= 0 or index > len(body):     # Если пользователь ввел индекс которого нет в списке, выходим из функции
            bot.send_message(message.chat.id, '❔ Такой заметки нет в списке')
            return
            
        for i in enumerate(body, 1):    # Ищем нужную нам запись
            if index != i[0]:           # Проверяем индекс введенный пользователем с индексом записи
                continue

            cur.execute(f"""DELETE FROM 'user.{message.chat.id}' WHERE time IN ('{i[1][0]}')""")     # Удаляем
            bot.send_message(message.chat.id, '❌ Я удалил твою заметку')
            logging.info(f'{message.chat.id:14} | Пользователь удалил заметку')
            break

        cur.execute(f"""SELECT * FROM 'user.{message.chat.id}'""")
        if cur.fetchall() == []:    # Если у пользователя нет записей после удаления, редактируем последний /list
            cur.execute(f"""SELECT listid FROM {TABLE} WHERE chatid = {message.chat.id}""")
            bot.edit_message_text(chat_id=message.chat.id, message_id=cur.fetchone()[0], text='У тебя нет дел 😔', parse_mode="Markdown")
            return

        cur.execute(f"""SELECT * FROM 'user.{message.chat.id}' ORDER BY time""")
    
        work = '📅 Список твоих дел:\n\n'
        for i in enumerate(cur.fetchall(), 1):
            j = i[1][0].split(' ')  # Разбиваем время напоминания по пробелам
            work = work + f"{i[0]}) {j[0][8:10]}.{j[0][5:7]}.{j[0][0:4]} в {j[1][:-3]} - {i[1][1]}\n"
        work = work + '\nЧтобы удалить пункт напиши - "Удалить (номер пункта)"'
        
        cur.execute(f"""SELECT listid FROM {TABLE} WHERE chatid = {message.chat.id}""")
        bot.edit_message_text(chat_id=message.chat.id, message_id=cur.fetchone()[0], text=work, parse_mode="Markdown")
