import sqlite3
import const
import telebot
import os

def reg(message):
    with sqlite3.connect('base.db') as db:
        cur = db.cursor()
        try:
            os.mkdir('voice/{}/'.format(str(message.chat.id)))
        except:
            pass
        cur.execute(u"""INSERT OR IGNORE INTO {} VALUES ({}, '{}', '{}', '{}', {}, {}, '{}')""".format(const.base, message.chat.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username, 0, const.timezone, u'voice/{}/'.format(message.chat.id)))
        cur.execute(u"""CREATE TABLE IF NOT EXISTS '{}' ('time'	TEXT, 'body' TEXT)""".format(message.chat.id))