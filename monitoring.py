# Функция для мониторинга времени
# Когда приходит время - отправляет напоминание пользователю
# Запускается в main после функции olddelete.py во второй поток

import const
import telebot
import json
from telebot import types
from datetime import datetime, timedelta

def monitoring():
    print ("Monitoring thread starting...")

    with open('base.json', 'r', encoding="utf-8") as f:
        copy_base = json.loads(f.read())

    while True:
        if const.copy != copy_base:
            with open('base.json', 'r', encoding="utf-8") as f:
                copy_base = json.loads(f.read())

        try:
            for k1 in copy_base:
                now = datetime.now() + timedelta(hours=int(copy_base[k1]["TZ"]))
                new_now = '{}.{}.{} {}:{}'.format(now.strftime("%Y"), now.strftime("%m"), now.strftime("%d"), now.strftime("%H"), now.strftime("%M"))

                for k2, v2 in copy_base[k1]["Work"].items():
                    if new_now in k2:
                        markup = types.InlineKeyboardMarkup()
                        button1 = types.InlineKeyboardButton('5 мин.', callback_data='1')
                        button2 = types.InlineKeyboardButton('15 мин.', callback_data='2')   
                        button3 = types.InlineKeyboardButton('30 мин.', callback_data='3')
                        button4 = types.InlineKeyboardButton('1 час.', callback_data='4')
                        button5 = types.InlineKeyboardButton('1 день.', callback_data='5')

                        markup.add(button1, button2, button3)
                        markup.add(button4, button5)

                        const.copy[k1]["WorkOut"][k2] = const.copy.get(k1).get("Work").get(k2)

                        print ('Я отправил - ' + str(const.copy.get(k1).get("Work").get(k2)))
                        const.bot.send_message(k1, text = const.copy.get(k1).get("Work").pop(k2), reply_markup = markup)
                        with open('base.json', 'w', encoding="utf-8") as ff:
                            json.dump(const.copy, ff, sort_keys=True, indent=4, ensure_ascii=False) 
        except:
            pass

