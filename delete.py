# Функция для удаления определенных записей, которые выберет пользователь
# Запускается во второй поток каждый раз когда пользователь вызывает Удаление Элемента

import telebot
import sqlite3
import re
from const import BASE
from datetime import datetime

def delet(message, bot):
    index = int(re.search(r'\d+', message.text).group()) - 1

    with sqlite3.connect('base.db') as db:
        cur = db.cursor()

        cur.execute(u"""SELECT * FROM '{}' ORDER BY time""".format(message.chat.id))
        body = [i for i in cur.fetchall()]
        n = 0
        if body != []:
            if 0 < index+1 <= len(body):
                for i in body:
                    if index == n:
                        cur.execute(u"""DELETE FROM '{}' WHERE time IN ('{}')""".format(message.chat.id, i[0]))
                        bot.send_message(message.chat.id, '❌ Я удалил твою заметку')

                        cur.execute(u"""SELECT * FROM '{}'""".format(message.chat.id))

                        if cur.fetchall() != []:
                            cur.execute(u"""SELECT * FROM '{}' ORDER BY time""".format(message.chat.id))
                        
                            work = '📅 Список твоих дел:\n\n'
                            

                            n = 1
                            for i in cur.fetchall():
                                work = work + str(n) + ') ' + i[0].split(' ')[0][8:10] + '.' + i[0].split(' ')[0][5:7] + '.' + i[0].split(' ')[0][0:4] + ' в '+ i[0].split(' ')[1][:-3] + ' - ' + i[1] + '\n'
                                n += 1

                            work = work + '\nЧтобы удалить пункт напиши - "Удалить (номер пункта)"'
                            
                            cur.execute(u"""SELECT listid FROM {} WHERE chatid = {}""".format(BASE, message.chat.id))
                            bot.edit_message_text(chat_id=message.chat.id, message_id=cur.fetchone()[0], text=work, parse_mode="Markdown")

                        else:
                            cur.execute(u"""SELECT listid FROM {} WHERE chatid = {}""".format(BASE, message.chat.id))
                            bot.edit_message_text(chat_id=message.chat.id, message_id=cur.fetchone()[0], text='У тебя нет дел 😔', parse_mode="Markdown")
                           
                    n += 1
            else:
                bot.send_message(message.chat.id, '❔ Такой заметки нет в списке')
        else:
            bot.send_message(message.chat.id, 'У тебя нет дел 😔')




    
      
    
