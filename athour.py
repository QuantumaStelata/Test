# Принимает сообщения типа:
# В X ТЕКСТ
# В X:Y ТЕКСТ

import telebot
import json
import const
import re
from oldbasedel import old_base_del
from datetime import datetime, timedelta
from threading import Thread

def athour(message):
    try:
        hour_minute = re.findall(r'(\d{1,2}[.|:|/]{0,1}\d{0,2})', message.text)[0]
        hour_minute = re.split(r'[.|:|/]', hour_minute)     # Получаем список [час, минут]

        hour = hour_minute[0]   # Час

        try:
            minute = hour_minute[1] if hour_minute[1] != '' else 0      # Минуты
        except:
            minute = 0      # Минуты
                
        text = message.text[re.search(r'(\d{1,2}[.|:|/]{0,1}\d{0,2})', message.text, re.IGNORECASE).end() + 0:].strip().capitalize() 
            
        now = datetime.now() + timedelta(hours = int(const.copy[str(message.chat.id)]["TZ"]))
        remind = datetime(int(now.year), int(now.month), int(now.day), int(hour), int(minute), int(now.second))

        if now > remind:
            remind = datetime(int(now.year), int(now.month), int(now.day) + 1, int(hour), int(minute), int(now.second))
            
        const.copy[str(message.chat.id)]["Work"][str(remind.strftime("%Y")) + '.' + str(remind.strftime("%m")) + '.' + str(remind.strftime("%d")) + ' ' + str(remind.strftime("%H")) + ':' + str(remind.strftime("%M")) + ':' + str(remind.strftime("%S"))] = text
        Thread(target=const.save).start()
        const.bot.send_message(message.chat.id, const.remind)
    except:
        const.bot.send_message(message.chat.id, const.not_understand)
        