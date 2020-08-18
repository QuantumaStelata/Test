import sqlite3
import const
import telebot
import os


def reg(message):
    with sqlite3.connect('base.db') as db:
        cur = db.cursor()
        try:
            os.mkdir('voice/{}/'.format(str(message.chat.id)))
        except:
            pass
        cur.execute(u"""INSERT OR IGNORE INTO base VALUES ({0}, '{1}', '{2}', '{3}', {4}, {5}, '{6}')""".format(message.chat.id, message.from_user.first_name, message.from_user.last_name, message.from_user.username, 0, const.timezone, u'voice/{}/'.format(message.chat.id)))
        #print (cur.fetchone()[0])

def reg1(message):
    if str(message.chat.id) not in const.copy.keys():
        with open('base.json', 'w', encoding="utf-8") as ff:
            try:
                os.mkdir('voice/{}/'.format(str(message.chat.id)))
            except:
                pass
            const.copy[str(message.chat.id)] = {"1Name": str(message.from_user.first_name), "2Name": str(message.from_user.last_name), "ID": str(message.from_user.username),"Voice": "voice/{}/".format(str(message.chat.id)),"TZ": str(const.timezone), "Work": {}}
            json.dump(const.copy, ff, sort_keys=True, indent=4, ensure_ascii=False)

