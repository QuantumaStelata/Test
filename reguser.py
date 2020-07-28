import json
import const
import telebot
import os
def reg(message):
    if str(message.chat.id) not in const.copy.keys():
        with open('base.json', 'w', encoding="utf-8") as ff:
            try:
                os.mkdir('voice/{}/'.format(str(message.chat.id)))
            except:
                pass
            
            const.copy[str(message.chat.id)] = {"1Name": str(message.from_user.first_name), "2Name": str(message.from_user.last_name), "ID": str(message.from_user.username),"Voice": "voice/{}/".format(str(message.chat.id)),"TZ": str(const.timezone), "List": 0, "Work": {}, "WorkOut": {}}
            json.dump(const.copy, ff, sort_keys=True, indent=4, ensure_ascii=False)
