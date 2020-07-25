# Принимает сообщения типа:
# Через X минут ТЕКСТ

import telebot
import json
import const
import re
from datetime import datetime, timedelta
from threading import Thread

def inminute(message):
    minutes = int(re.search(r'\d+', message.text).group())
    text = message.text[re.search(r'\bминут[уы]?', message.text, re.IGNORECASE).end() + 0:].strip().capitalize()

    remind = datetime.now() + timedelta(hours = int(const.copy[str(message.chat.id)]["TZ"]), minutes=minutes)
    const.copy[str(message.chat.id)]["Work"][str(remind.strftime("%Y")) + '.' + str(remind.strftime("%m")) + '.' + str(remind.strftime("%d")) + ' ' + str(remind.strftime("%H")) + ':' + str(remind.strftime("%M")) + ':' + str(remind.strftime("%S"))] = text

    Thread(target=const.save).start()       
    const.bot.send_message(message.chat.id, const.remind)

