import telebot
import sqlite3
from const import TOKEN
from requests import get
    
def sticker(message, bot): 
    stickerid = bot.get_file(message.sticker.file_id).file_path       # Хранит ID стикера
    print (stickerid)

    print (stickerid)
    with sqlite3.connect('base.db') as db:
        cur = db.cursor()  
        cur.execute(u"""SELECT * FROM stickers""")
        
        for i in cur.fetchall():
            if i[0] == stickerid:
                message.text = i[1]
            else:
                message.text = "None"
                
        
        #print(message.text)

#bot.send_sticker(message.chat.id, 'CAACAgUAAxkBAAIBtF8W4mnS44I1futOLOabjzGI5BuJAAL_AANxffwUdic7ErtbrcEaBA')