import sqlite3
from const import BASE, TABLE
from datetime import datetime, timedelta
from log.logger import logging


def old_base_del():
    '''
    Функция для удаления устаревших записей пользователей
    Запускается в main перед началом работы основных функций
    '''
    
    logging.info(f'{"":14} | Запуск цикла очистки базы данных от старых записей')
    with sqlite3.connect(BASE) as db:
        cur = db.cursor()

        cur.execute(f"""SELECT chatid, timezone FROM {TABLE}""")
        
        for i in cur.fetchall():
            cur.execute(f"""SELECT * FROM 'user.{i[0]}'""")
            now = datetime.now() + timedelta(hours = i[1])
            for remind in cur.fetchall():
                data = datetime(int(remind[0][0:4]), int(remind[0][5:7]), int(remind[0][8:10]), int(remind[0][11:13]), int(remind[0][14:16]), int(remind[0][17:19]))
                if now > data:
                    cur.execute(f"""DELETE FROM 'user.{i[0]}' WHERE time IN ('{remind[0]}')""")

    logging.info(f'{"":14} | База данных очищена от старых записей')