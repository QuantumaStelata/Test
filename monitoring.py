import sqlite3
import telebot
from const import BASE, TABLE
from datetime import datetime, timedelta
from log.logger import *

def monitoring(bot):
    '''
    Функция для мониторинга времени
    Когда приходит время - отправляет напоминание пользователю
    Запускается в main после функции olddelete.py 
    '''
    
    logging.info(f'{"":14} | Запуск цикла мониторинга')
    while True:
        with sqlite3.connect(BASE) as db:
            cur = db.cursor()

            cur.execute(f"""SELECT chatid, timezone FROM {TABLE}""")

            for i in cur.fetchall():
                now = datetime.now() + timedelta(hours=i[1])
                new_now = f'{now.strftime("%Y")}.{now.strftime("%m")}.{now.strftime("%d")} {now.strftime("%H")}:{now.strftime("%M")}'
                cur.execute(f"""SELECT * FROM 'user.{i[0]}'""")
                for remind in cur.fetchall():
                    if new_now in remind[0]:
                        bot.send_message(i[0], text = remind[1])
                        cur.execute(f"""DELETE FROM 'user.{i[0]}' WHERE time IN ('{remind[0]}')""")
                        logging.info(f'{i[0]:14} | Отправлено напоминание - {remind[1]}')