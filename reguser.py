import sqlite3
import telebot
from os import mkdir
from const import BASE


def reg(message, timezone):
    with sqlite3.connect("base.db") as db:
        cur = db.cursor()
        try:
            mkdir("voice/{}/".format(str(message.chat.id)))
        except:
            pass
        
        cur.execute(
            u"""INSERT OR IGNORE INTO {} VALUES ({}, '{}', '{}', '{}', {}, {}, '{}')""".format(BASE, message.chat.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username, 0, timezone, u"voice/{}/".format(message.chat.id)))
        
        cur.execute(
            u"""CREATE TABLE IF NOT EXISTS '{}' ('time'	TEXT, 'body' TEXT)""".format(message.chat.id))

