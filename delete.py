# Функция для удаления определенных записей, которые выберет пользователь
# Так же редактирует последний вызванный /list после удаления записи

import telebot
import sqlite3
import re
from const import BASE
from datetime import datetime
from log.logger import *

def delet(message, bot):
    index = int(re.search(r'\d+', message.text).group())

    with sqlite3.connect('base.db') as db:
        cur = db.cursor()
        cur.execute(f"""SELECT * FROM 'user.{message.chat.id}' ORDER BY time""")
        body = [i for i in cur.fetchall()]      # Получаем список записок пользователя
        
        if body == []:      # Если у пользователя нет записи, выходим из функции
            bot.send_message(message.chat.id, 'У тебя нет дел 😔')
            return
        
        if index <= 0 or index > len(body):     # Если пользователь ввел индекс которого нет в списке, выходим из функции
            bot.send_message(message.chat.id, '❔ Такой заметки нет в списке')
            return
            
        for i in enumerate(body, 1):    # Ищем нужную нам запись
            if index != i[0]:           # Проверяем индекс введенный пользователем с индексом записи
                continue

            cur.execute(f"""DELETE FROM 'user.{message.chat.id}' WHERE time IN ('{i[1][0]}')""")     # Удаляем
            bot.send_message(message.chat.id, '❌ Я удалил твою заметку')
        logging.info(f'Пользователь {message.chat.id} удалил заметку')

        cur.execute(f"""SELECT * FROM 'user.{message.chat.id}'""")
        if cur.fetchall() == []:    # Если у пользователя нет записей после удаления, редактируем последний /list
            cur.execute(f"""SELECT listid FROM {BASE} WHERE chatid = {message.chat.id}""")
            bot.edit_message_text(chat_id=message.chat.id, message_id=cur.fetchone()[0], text='У тебя нет дел 😔', parse_mode="Markdown")
            return

        cur.execute(f"""SELECT * FROM 'user.{message.chat.id}' ORDER BY time""")
    
        work = '📅 Список твоих дел:\n\n'
        for i in enumerate(cur.fetchall(), 1):
            j = i[1][0].split(' ')  # Разбиваем время напоминания по пробелам
            work = work + f"{i[0]}) {j[0][8:10]}.{j[0][5:7]}.{j[0][0:4]} в {j[1][:-3]} - {i[1][1]}\n"
        work = work + '\nЧтобы удалить пункт напиши - "Удалить (номер пункта)"'
        
        cur.execute(f"""SELECT listid FROM {BASE} WHERE chatid = {message.chat.id}""")
        bot.edit_message_text(chat_id=message.chat.id, message_id=cur.fetchone()[0], text=work, parse_mode="Markdown")

                
                    

        




    
      
    
