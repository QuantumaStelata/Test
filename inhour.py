# Принимает сообщения типа:
# Через X часов ТЕКСТ

import telebot
import json
import const
import re
from datetime import datetime, timedelta
from threading import Thread


def inhour(message):
    hours = int(re.search(r'\d+', message.text).group())
    text = message.text[re.search(r'\bчас[ао]*[в]?', message.text, re.IGNORECASE).end() + 0:].strip().capitalize()
                
    remind = datetime.now() + timedelta(hours=hours + int(const.copy[str(message.chat.id)]["TZ"]))
    const.copy[str(message.chat.id)]["Work"][str(remind.strftime("%Y")) + '.' + str(remind.strftime("%m")) + '.' + str(remind.strftime("%d")) + ' ' + str(remind.strftime("%H")) + ':' + str(remind.strftime("%M")) + ':' + str(remind.strftime("%S"))] = text
               
    Thread(target=const.save).start()
    const.bot.send_message(message.chat.id, const.remind)