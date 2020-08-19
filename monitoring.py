# Функция для мониторинга времени
# Когда приходит время - отправляет напоминание пользователю
# Запускается в main после функции olddelete.py во второй поток

import sqlite3
import const
import telebot
from datetime import datetime, timedelta


def monitoring():
    print ("Monitoring thread starting...")
    while True:
        with sqlite3.connect('base.db') as db:
            cur = db.cursor()

            cur.execute(u"""SELECT chatid, timezone FROM {}""".format(const.base))

            for i in cur.fetchall():
                now = datetime.now() + timedelta(hours=i[1])
                new_now = '{}.{}.{} {}:{}'.format(now.strftime("%Y"), now.strftime("%m"), now.strftime("%d"), now.strftime("%H"), now.strftime("%M"))
                cur.execute(u"""SELECT * FROM '{0}'""".format(i[0]))
                for remind in cur.fetchall():
                    if new_now in remind[0]:
                        print ('Я отправил - ' + remind[1])
                        const.bot.send_message(i[0], text = remind[1])
                        cur.execute(u"""DELETE FROM '{}' WHERE time IN ('{}')""".format(i[0], remind[0]))

