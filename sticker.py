import telebot
import sqlite3
from const import BASE, NOT_PREMIUM

def sticker(message, bot): 
    stickerid = message.json['sticker']['thumb']['file_unique_id']       # Хранит ID стикера

    with sqlite3.connect('base.db') as db:
        cur = db.cursor()
        cur.execute(f"""SELECT premium FROM {BASE} WHERE chatid = {message.chat.id}""")

        if cur.fetchone()[0] != 'Yes':      # Проверка на наличие премиум аккаунта.
            message.text = "Sticker.py/Message.text/None"
            bot.send_sticker(message.chat.id, 'CAACAgUAAxkBAAIBtF8W4mnS44I1futOLOabjzGI5BuJAAL_AANxffwUdic7ErtbrcEaBA')
            bot.send_message(message.chat.id, NOT_PREMIUM)

        cur.execute(u"""SELECT * FROM stickers""")
        
        for i in cur.fetchall():
            if i[0] != '*' and i[0] != message.chat.id:
                message.text = "Sticker.py/Message.text/None"
                continue
                
            if i[1] != stickerid:
                message.text = "Sticker.py/Message.text/None"
                continue

            message.text = i[2]
            return     