import telebot
from threading import Thread

import re
import sqlite3

import const

from content_message_commands import reg, list_
from content_message_text import atdate, athour, inhour, inminute, delet
from content_message_other import sticker, voice

from oldbasedel import old_base_del
from monitoring import monitoring   

from log.logger import *

bot = telebot.TeleBot(const.TOKEN)


@bot.message_handler(commands=["start"])
def command_start(message):
    bot.send_message(message.chat.id, const.START, parse_mode="Markdown")

    with sqlite3.connect('base.db') as db:
        cur = db.cursor()

        cur.execute(f"""SELECT chatid FROM {const.BASE}""")
        chatid = [i[0] for i in cur.fetchall()]

        if message.chat.id not in chatid:
            msg = bot.send_message(message.chat.id, const.TIMEZONETEXT, parse_mode="Markdown")
            bot.register_next_step_handler(msg, tz)
        
def tz(message):
    try:
        timezone = int(message.text)
        if 12 >= timezone >= -12:
            Thread(target=reg, args = (message, timezone)).start()
            bot.send_message(message.chat.id, '✅ Часовой пояс установлен.')
        else:
            msg = bot.send_message(message.chat.id, 'Что-то не так! Попробуйте еще раз ввести свой часовой пояс...')
            bot.register_next_step_handler(msg, tz)
            return
    except:
        msg = bot.send_message(message.chat.id, 'Что-то не так! Попробуйте еще раз ввести свой часовой пояс...')
        bot.register_next_step_handler(msg, tz)


@bot.message_handler(commands=["time"])
def command_time(message):
    msg = bot.send_message(message.chat.id, const.TIMEZONETEXT)
    bot.register_next_step_handler(msg, changetz)

def changetz(message):
    try:
        timezone = int(message.text)
        if 12 >= timezone >= -12:
            with sqlite3.connect('base.db') as db:
                db.cursor().execute(f"""UPDATE {const.BASE} SET timezone = {timezone} WHERE chatid = {message.chat.id}""")
                bot.send_message(message.chat.id, '✅ Часовой пояс установлен.')
                logging.info(f'{message.chat.id:14} | Пользователь поменял timezone на {timezone}')
        else:
            msg = bot.send_message(message.chat.id, 'Что-то не так! Попробуйте еще раз...')
            bot.register_next_step_handler(msg, changetz)
    except:
        msg = bot.send_message(message.chat.id, 'Что-то не так! Попробуйте еще раз...')
        bot.register_next_step_handler(msg, changetz)


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
def commands(message):
    bot.send_message(message.chat.id, const.COMMANDS, parse_mode="Markdown")
    logging.info(f'{message.chat.id:14} | Пользователь запустил /commands')


@bot.message_handler(commands=["list"])
def command_new(message):
    list_(message, bot)


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
    logging.debug(f'{message.chat.id:14} | Пользователь отправил - {message.text}')
    
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
    const.push(bot)                     # Рассылка по всем пользователям
    old_base_del()                      # Удаление старых записей
    Thread(target=monitoring, args=(bot,)).start()   # Запуск 2-ого потока - функция monitoring из monitoring.py
    logging.info(f'{"":14} | Запуск цикла обработки событий')
    bot.infinity_polling()
