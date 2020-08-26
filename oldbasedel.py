# Функция для удаления устаревших записей пользователей
# Запускается в main перед началом работы основных функций

import sqlite3
from const import BASE
from datetime import datetime, timedelta
from log.logger import *


def old_base_del():
    logging.info('Запуск цикла очистки базы данных от старых записей')
    with sqlite3.connect('base.db') as db:
        cur = db.cursor()

        cur.execute(u"""SELECT chatid, timezone FROM {}""".format(BASE))
        
        for i in cur.fetchall():
            cur.execute(u"""SELECT * FROM 'user.{0}'""".format(i[0]))
            now = datetime.now() + timedelta(hours = i[1])
            for remind in cur.fetchall():
                data = datetime(int(remind[0][0:4]), int(remind[0][5:7]), int(remind[0][8:10]), int(remind[0][11:13]), int(remind[0][14:16]), int(remind[0][17:19]))
                if now > data:
                    cur.execute(u"""DELETE FROM 'user.{}' WHERE time IN ('{}')""".format(i[0], remind[0]))

    logging.info('База данных очищена от старых записей')