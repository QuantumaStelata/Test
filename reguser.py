import sqlite3
import telebot
from os import mkdir
from const import BASE
from log.logger import *

def reg(message, timezone):
    with sqlite3.connect("base.db") as db:
        cur = db.cursor()
        try:
            dir = f"voice/{message.chat.id}/"
            mkdir(dir)
        except:
            logging.warning(f'{message.chat.id:14} | Папка уже создана для пользователя')
        
        cur.execute(
            f"""INSERT OR IGNORE INTO {BASE} VALUES ({message.chat.id}, 'No', '{message.from_user.first_name}', '{message.from_user.last_name}', '{message.from_user.username}', 0, {timezone}, '{dir}')""")
        
        cur.execute(
            f"""CREATE TABLE IF NOT EXISTS 'user.{message.chat.id}' ('time' TEXT, 'body' TEXT)""")

        logging.info(f'{message.chat.id:14} | Новый пользователь')