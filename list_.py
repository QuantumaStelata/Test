import telebot
import sqlite3
from const import BASE

def list_(message, bot):
    with sqlite3.connect('base.db') as db:
        cur = db.cursor()

        cur.execute(u"""SELECT * FROM 'user.{}'""".format(message.chat.id))

        if cur.fetchall() != []:
            cur.execute(u"""SELECT * FROM 'user.{}' ORDER BY time""".format(message.chat.id))
        
            work = '📅 Список твоих дел:\n\n'
            

            n = 1
            for i in cur.fetchall():
                work = work + str(n) + ') ' + i[0].split(' ')[0][8:10] + '.' + i[0].split(' ')[0][5:7] + '.' + i[0].split(' ')[0][0:4] + ' в '+ i[0].split(' ')[1][:-3] + ' - ' + i[1] + '\n'
                n += 1

            work = work + '\nЧтобы удалить пункт напиши - "Удалить (номер пункта)"'
            bot.send_message(message.chat.id, work, parse_mode="Markdown")
            cur.execute(u"""UPDATE '{}' SET listid = {} WHERE chatid = {}""".format(BASE, message.message_id + 1, message.chat.id))

        else:
            bot.send_message(message.chat.id, 'У тебя нет дел 😔', parse_mode="Markdown")