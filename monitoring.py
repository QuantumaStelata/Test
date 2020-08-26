# Функция для мониторинга времени
# Когда приходит время - отправляет напоминание пользователю
# Запускается в main после функции olddelete.py 

import sqlite3
import telebot
from const import BASE
from datetime import datetime, timedelta
from log.logger import *

def monitoring(bot):
    logging.info('Запуск цикла мониторинга')
    while True:
        with sqlite3.connect('base.db') as db:
            cur = db.cursor()

            cur.execute(u"""SELECT chatid, timezone FROM {}""".format(BASE))

            for i in cur.fetchall():
                now = datetime.now() + timedelta(hours=i[1])
                new_now = '{}.{}.{} {}:{}'.format(now.strftime("%Y"), now.strftime("%m"), now.strftime("%d"), now.strftime("%H"), now.strftime("%M"))
                cur.execute(u"""SELECT * FROM 'user.{0}'""".format(i[0]))
                for remind in cur.fetchall():
                    if new_now in remind[0]:
                        bot.send_message(i[0], text = remind[1])
                        cur.execute(u"""DELETE FROM 'user.{}' WHERE time IN ('{}')""".format(i[0], remind[0]))
                        logging.info(f'Отправлено напоминание - {remind[1]}, пользователю - {i[0]}')