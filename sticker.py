import telebot
import sqlite3
from const import BASE, NOT_PREMIUM

def sticker(message, bot): 
    stickerid = message.json['sticker']['thumb']['file_unique_id']       # Хранит ID стикера
    
    with sqlite3.connect('base.db') as db:
        cur = db.cursor()
        cur.execute(u"""SELECT premium FROM {} WHERE chatid = {}""".format(BASE, message.chat.id))

        if cur.fetchone()[0] == 'Yes':      # Проверка на наличие премиум аккаунта.
            cur.execute(u"""SELECT * FROM stickers""")
            
            for i in cur.fetchall():
                if i[0] == stickerid:
                    message.text = i[1]
                    break
                else:
                    message.text = "Sticker.py/Message.text/None"
        else:
            message.text = "Sticker.py/Message.text/None"
            bot.send_sticker(message.chat.id, 'CAACAgUAAxkBAAIBtF8W4mnS44I1futOLOabjzGI5BuJAAL_AANxffwUdic7ErtbrcEaBA')
            bot.send_message(message.chat.id, NOT_PREMIUM)
                