import sqlite3
import telebot
from os import mkdir
from const import BASE, TABLE
from log.logger import logging

def reg_user(message, timezone):
    '''
    Регистрация пользователя командой /start
    '''

    with sqlite3.connect("base.db") as db:
        cur = db.cursor()
        try:
            dir = f"voice/{message.chat.id}/"
            mkdir(dir)
        except:
            logging.warning(f'{message.chat.id:14} | Папка уже создана для пользователя')
        
        cur.execute(
            f"""INSERT OR IGNORE INTO {TABLE} VALUES ({message.chat.id}, 'No', '{message.from_user.first_name}', '{message.from_user.last_name}', '{message.from_user.username}', 0, {timezone}, '{dir}')""")
        
        cur.execute(
            f"""CREATE TABLE IF NOT EXISTS 'user.{message.chat.id}' ('time' TEXT, 'body' TEXT)""")

        logging.info(f'{message.chat.id:14} | Новый пользователь')


def list_user(message, bot):
    '''
    Команда /list. Список записей пользователя
    '''
    
    with sqlite3.connect(BASE) as db:
        cur = db.cursor()

        cur.execute(f"""SELECT * FROM 'user.{message.chat.id}'""")

        if cur.fetchall() == []:
            bot.send_message(message.chat.id, 'У тебя нет дел 😔', parse_mode="Markdown")
            return

        cur.execute(f"""SELECT * FROM 'user.{message.chat.id}' ORDER BY time""")
        
        work = '📅 Список твоих дел:\n\n'
        for i in enumerate(cur.fetchall(), 1):
            j = i[1][0].split(' ')  # Разбиваем время напоминания по пробелам
            work = work + f"{i[0]}) {j[0][8:10]}.{j[0][5:7]}.{j[0][0:4]} в {j[1][:-3]} - {i[1][1]}\n"
        work = work + '\nЧтобы удалить пункт напиши - "Удалить (номер пункта)"'
        
        bot.send_message(message.chat.id, work, parse_mode="Markdown")
        cur.execute(f"""UPDATE '{TABLE}' SET listid = {message.message_id + 1} WHERE chatid = {message.chat.id}""")
        logging.info(f'{message.chat.id:14} | Пользователь запустил /list')