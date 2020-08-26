import sqlite3
import telebot
from os import mkdir
from const import BASE
from log.logger import *

def reg(message, timezone):
    with sqlite3.connect("base.db") as db:
        cur = db.cursor()
        try:
            mkdir(f"voice/{message.chat.id}/")
        except:
            logging.warning(f'Папка уже создана для пользователя {message.chat.id}')
        
        cur.execute(
            u"""INSERT OR IGNORE INTO {} VALUES ({}, '{}', '{}', '{}', '{}', {}, {}, '{}')""".format(BASE, message.chat.id, u'No', message.from_user.first_name, message.from_user.last_name, message.from_user.username, 0, timezone, u"voice/{}/".format(message.chat.id)))
        
        cur.execute(
            u"""CREATE TABLE IF NOT EXISTS 'user.{}' ('time' TEXT, 'body' TEXT)""".format(message.chat.id))

        logging.info(f'Новый пользователь - {message.chat.id}')