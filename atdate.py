# Принимает сообщения типа:
# %D.$M.%Y в %H.%M ТЕКСТ
# %D.$M.%Y %H.%M ТЕКСТ
# %D.$M.%Y в %H ТЕКСТ
# %D.$M.%Y %H ТЕКСТ

# Допускаемые символы . : / 

import telebot
import sqlite3
import re
from const import REMIND
from oldbasedel import old_base_del
from datetime import datetime, timedelta
from threading import Thread

def atdate(message, bot):
    date = re.search(r'(\d{1,2}[.|:|/]{1}\d{1,2}[.|:|/]{1}\d{2,4})', message.text).group()  # Получаем дату
    time = re.findall(r'(\d{1,2}[.|:|/]{0,1}\d{0,2})', message.text.replace(date,''))[0]    # Получаем время

    date = re.split(r'[.|:|/]', date)   # Получаем список [число, месяц, год]
    time = re.split(r'[.|:|/]', time)   # Получаем список [час, минут]

    day = int(date[0])      # Получаем день
    month = int(date[1])    # Получаем месяц
    year = int(date[2]) if len(date[2]) == 4 else int("20" + str(date[2]))  # В случае если год указан 2-ух значно -> добавляет впереди 20
  
    hour = int(time[0])     # Получаем час
    minute = int(time[1]) if len(time) > 1 else 0   # В случае если минуты не указаны присваевается 0
    
    text = message.text[re.search(r'(\d{1,2}[.|:|/]{1}\d{1,2}[.|:|/]{1}\d{2,4})(\s*)([в]\s*)?(\d{1,2}[.|:|/]{0,1}\d{0,2})', message.text, re.IGNORECASE).end() + 0:].strip().capitalize()

    now = datetime.now()
    remind_ = datetime(year, month, day, hour, minute, int(now.second))
    remind_text = str(remind_.strftime("%Y")) + '.' + str(remind_.strftime("%m")) + '.' + str(remind_.strftime("%d")) + ' ' + str(remind_.strftime("%H")) + ':' + str(remind_.strftime("%M")) + ':' + str(remind_.strftime("%S"))

    with sqlite3.connect('base.db') as db:
        cur = db.cursor()  
        cur.execute(u"""INSERT INTO '{}' VALUES ('{}', '{}')""".format(message.chat.id, remind_text, text))

    bot.send_message(message.chat.id, REMIND)
   

