import telebot
from telebot import types
from threading import Thread

import re
import sqlite3

import const

from content_message_commands import reg_user, change_geo, list_user
from content_message_text import atdate, athour, inhour, inminute, delet
from content_message_other import push, sticker, voice, weather

from oldbasedel import old_base_del
from monitoring import monitoring   

from log.logger import logging

bot = telebot.TeleBot(const.TOKEN)


@bot.message_handler(commands=["start"])
def command_start(message):
    bot.send_message(message.chat.id, const.START, parse_mode="Markdown")

    with sqlite3.connect(const.BASE) as db:
        cur = db.cursor()

        cur.execute(f"""SELECT chatid FROM {const.TABLE}""")
        chatid = [i[0] for i in cur.fetchall()]

        if message.chat.id not in chatid:
            keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
            keyboard.add(button_geo)

            msg = bot.send_message(message.chat.id, const.GEOLOCTEXT, parse_mode="Markdown", reply_markup=keyboard)
            bot.register_next_step_handler(msg, location)


@bot.message_handler(commands=["time"])
def command_time(message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_geo = types.KeyboardButton(text="Отправить местоположение", request_location=True)
    keyboard.add(button_geo)

    msg = bot.send_message(message.chat.id, const.GEOLOCTEXT, parse_mode="Markdown", reply_markup=keyboard)
    bot.register_next_step_handler(msg, location)


@bot.message_handler(content_types=["location"])
def location(message):
    with sqlite3.connect(const.BASE) as db:
        cur = db.cursor()

        cur.execute(f"""SELECT chatid FROM {const.TABLE}""")
        chatid = [i[0] for i in cur.fetchall()]
        
        if message.chat.id not in chatid:
            if message.location is not None:
                Thread(target=reg_user, args = (message,)).start()
                bot.send_message(message.chat.id, '✅ Часовой пояс установлен.', reply_markup=types.ReplyKeyboardRemove())
                return
            
            msg = bot.send_message(message.chat.id, const.GEOLOCTEXT)
            bot.register_next_step_handler(msg, location)
            return
        
        if message.location is not None:
            Thread(target=change_geo, args = (message, bot)).start()
            bot.send_message(message.chat.id, '✅ Часовой пояс установлен.', reply_markup=types.ReplyKeyboardRemove())
            return
        
        msg = bot.send_message(message.chat.id, const.GEOLOCTEXT)
        bot.register_next_step_handler(msg, location)


@bot.message_handler(commands=["sticker"])
def command_sticker(message):
    bot.send_message(message.chat.id, const.STICKERTEXT)
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAIKuV9DzidsQQwkrLf8uVJCwyfaTqhzAAIBAAP00Q8Y2Vj_yRX8h3IbBA')
    logging.info(f'{message.chat.id:14} | Пользователь запустил /sticker')


@bot.message_handler(commands=["callback"])
def command_callback(message):
    msg = bot.send_message(message.chat.id, const.CALLBACKTEXT, parse_mode="Markdown")
    bot.register_next_step_handler(msg, callback)

def callback(message):
    bot.send_message(const.ADMINID, f'@{message.from_user.username}\nChatId - {message.chat.id}\n\n{message.text}', parse_mode="Markdown")
    bot.send_message(message.chat.id, 'Я отправил, спасибо за обращение 👌', parse_mode="Markdown")
    logging.info(f'{message.chat.id:14} | Пользователь отправил callback с текстом - {message.text}')


@bot.message_handler(commands=["commands"])
def command_commands(message):
    bot.send_message(message.chat.id, const.COMMANDS, parse_mode="Markdown")
    logging.info(f'{message.chat.id:14} | Пользователь запустил /commands')


@bot.message_handler(commands=["list"])
def command_list(message):
    list_user(message, bot)


@bot.message_handler(commands=["weather"])
def command_weather(message):
    weather(message, bot)
    logging.info(f'{message.chat.id:14} | Пользователь запустил /weather')


@bot.message_handler(content_types=["sticker"])
def mainsticker(message):
    logging.info(f'{message.chat.id:14} | Пользователь отправил стикер')
    sticker(message, bot)
    main(message)
    

@bot.message_handler(content_types=["voice"])
def mainvoice(message):
    logging.info(f'{message.chat.id:14} | Пользователь отправил голосовое сообщение')
    voice(message, bot)
    main(message)


@bot.message_handler(content_types=["text"])
def main(message):
    logging.info(f'{message.chat.id:14} | Пользователь отправил - {message.text}')
    
    if re.search(r'(\d{1,2})[.|:|/](\d{1,2})[.|:|/](\d{4}|\d{2})\s+(в\s*)?(\d{1,2})[.|:|/]?(\d{0,2})\s*(.*)', message.text, re.IGNORECASE):
        logging.info(f'{message.chat.id:14} | Пользователь отправил - {message.text}')
        Thread(target=atdate, args=(message, bot)).start()
    
    elif re.search(r'(в)\s+(\d{1,2})([.|:|/]?)(\d{0,2})\s*(.*)', message.text, re.IGNORECASE):
        logging.info(f'{message.chat.id:14} | Пользователь отправил - {message.text}')
        Thread(target=athour, args=(message, bot)).start()

    elif re.search(r'(через)\s+(\d+)\s+(минут[уы]?)\s*(.*)', message.text, re.IGNORECASE):
        logging.info(f'{message.chat.id:14} | Пользователь отправил - {message.text}')
        Thread(target=inminute, args=(message, bot)).start()
            
    elif re.search(r'(через)\s+(\d+)\s+(час[ао]?[в]?)\s*(.*)', message.text, re.IGNORECASE):
        logging.info(f'{message.chat.id:14} | Пользователь отправил - {message.text}')
        Thread(target=inhour, args=(message, bot)).start()
        
    elif re.search(r'удалить.?\d+', message.text, re.IGNORECASE):
        Thread(target=delet, args=(message, bot)).start()

    else:
        if message.chat.id > 0 and message.text != 'Sticker.py/Message.text/None':
            bot.send_message(message.chat.id, const.NOT_UNDERSTAND)


if __name__ == '__main__':
    push(bot)                     # Рассылка по всем пользователям
    old_base_del()                # Удаление старых записей
    Thread(target=monitoring, args=(bot,)).start()   # Запуск 2-ого потока - функция monitoring из monitoring.py
    logging.info(f'{"":14} | Запуск цикла обработки событий')
    bot.infinity_polling()
