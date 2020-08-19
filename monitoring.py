# Функция для мониторинга времени
# Когда приходит время - отправляет напоминание пользователю
# Запускается в main после функции olddelete.py во второй поток

import sqlite3
import const
import telebot
import json
from time import sleep
from datetime import datetime, timedelta

def monitoring():
    print ("Monitoring thread starting...")
    while True:
        with sqlite3.connect('base.db') as db:
            cur = db.cursor()

            cur.execute(u"""SELECT chatid, timezone FROM base""")

            for i in cur.fetchall():
                now = datetime.now() + timedelta(hours=i[1])
                new_now = '{}.{}.{} {}:{}'.format(now.strftime("%Y"), now.strftime("%m"), now.strftime("%d"), now.strftime("%H"), now.strftime("%M"))
                print (new_now)
                cur.execute(u"""SELECT * FROM '{0}'""".format(i[0]))
                for j in cur.fetchall():
                    if new_now in j[0]:
                        print ('Я отправил - ' + j[1])
                        const.bot.send_message(k1, text = j[1])


def monitoring1():
    print ("Monitoring thread starting...")
    while True: 
        try:
            for k1 in const.copy:
                now = datetime.now() + timedelta(hours=int(const.copy[k1]["TZ"]))
                new_now = '{}.{}.{} {}:{}'.format(now.strftime("%Y"), now.strftime("%m"), now.strftime("%d"), now.strftime("%H"), now.strftime("%M"))

                for k2, v2 in const.copy[k1]["Work"].items():
                    if new_now in k2:
                        print ('Я отправил - ' + str(const.copy.get(k1).get("Work").get(k2)))
                        const.bot.send_message(k1, text = const.copy.get(k1).get("Work").pop(k2))
                        with open('base.json', 'w', encoding="utf-8") as ff:
                            json.dump(const.copy, ff, sort_keys=True, indent=4, ensure_ascii=False) 
        except:
            pass

