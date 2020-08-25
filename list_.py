import telebot
import sqlite3
from const import BASE

def list_(message, bot):
    with sqlite3.connect('base.db') as db:
        cur = db.cursor()

        cur.execute(u"""SELECT * FROM 'user.{}'""".format(message.chat.id))

        if cur.fetchall() == []:
            bot.send_message(message.chat.id, 'У тебя нет дел 😔', parse_mode="Markdown")
            return

        cur.execute(u"""SELECT * FROM 'user.{}' ORDER BY time""".format(message.chat.id))
        
        work = '📅 Список твоих дел:\n\n'
        for i in enumerate(cur.fetchall(), 1):
            j = i[1][0].split(' ')  # Разбиваем время напоминания по пробелам
            work = work + f"{i[0]}) {j[0][8:10]}.{j[0][5:7]}.{j[0][0:4]} в {j[1][:-3]} - {i[1][1]}\n"
        work = work + '\nЧтобы удалить пункт напиши - "Удалить (номер пункта)"'
        
        bot.send_message(message.chat.id, work, parse_mode="Markdown")
        cur.execute(u"""UPDATE '{}' SET listid = {} WHERE chatid = {}""".format(BASE, message.message_id + 1, message.chat.id))

        
            