# Принимает сообщения типа:
# %D.$M.%Y в %H.%M ТЕКСТ
# %D.$M.%Y %H.%M ТЕКСТ
# %D.$M.%Y в %H ТЕКСТ
# %D.$M.%Y %H ТЕКСТ

# Допускаемые символы . : / 

import telebot
import json
import re
from const base, remind
from oldbasedel import old_base_del
from datetime import datetime, timedelta
from threading import Thread

def atdate(message):
    date = re.search(r'(\d{1,2}[.|:|/]{1}\d{1,2}[.|:|/]{1}\d{2,4})', message.text).group()  # Получаем дату
    time = re.findall(r'(\d{1,2}[.|:|/]{0,1}\d{0,2})', message.text.replace(date,''))[0]    # Получаем время

    date = re.split(r'[.|:|/]', date)   # Получаем список [число, месяц, год]
    time = re.split(r'[.|:|/]', time)   # Получаем список [час, минут]

    day = int(date[0])
    month = int(date[1])
    year = int(date[2]) if len(date[2]) == 4 else int("20" + str(date[2]))  # В случае если год указан 2-ух значно -> добавляет впереди 20
  
    hour = int(time[0])
    minute = int(time[1]) if len(time) > 1 else 0   # В случае если минуты не указаны присваевается 0
    
    text = message.text[re.search(r'(\d{1,2}[.|:|/]{1}\d{1,2}[.|:|/]{1}\d{2,4})(\s*)([в]\s*)?(\d{1,2}[.|:|/]{0,1}\d{0,2})', message.text, re.IGNORECASE).end() + 0:].strip().capitalize()

    now = datetime.now()
    remind = datetime(year, month, day, hour, minute, int(now.second))
    
    const.copy[str(message.chat.id)]["Work"][str(remind.strftime("%Y")) + '.' + str(remind.strftime("%m")) + '.' + str(remind.strftime("%d")) + ' ' + str(remind.strftime("%H")) + ':' + str(remind.strftime("%M")) + ':' + str(remind.strftime("%S"))] = text

    Thread(target=const.save).start()
    Thread(target=old_base_del).start()
    const.bot.send_message(message.chat.id, const.remind)
   

