import telebot
import sqlite3

import speech_recognition as sr
from requests import get
from subprocess import run

from const import BASE, TABLE, NOT_PREMIUM, TOKEN


def sticker(message, bot):
    '''
    Функция обработки сообщений - стикеров
    '''

    stickerid = message.json['sticker']['thumb']['file_unique_id']       # Хранит ID стикера

    with sqlite3.connect(BASE) as db:
        cur = db.cursor()
        cur.execute(f"""SELECT premium FROM {TABLE} WHERE chatid = {message.chat.id}""")

        if cur.fetchone()[0] != 'Yes':      # Проверка на наличие премиум аккаунта.
            message.text = "Sticker.py/Message.text/None"
            bot.send_sticker(message.chat.id, 'CAACAgUAAxkBAAIBtF8W4mnS44I1futOLOabjzGI5BuJAAL_AANxffwUdic7ErtbrcEaBA')
            bot.send_message(message.chat.id, NOT_PREMIUM)
            return

        cur.execute(u"""SELECT * FROM stickers""")
        
        for i in cur.fetchall():
            if i[0] != '*' and i[0] != message.chat.id:
                message.text = "Sticker.py/Message.text/None"
                continue
                
            if i[1] != stickerid:
                message.text = "Sticker.py/Message.text/None"
                continue

            message.text = i[2]
            return     


def voice(message, bot):
    '''
    Принимает голосовое сообщение
    Скачивает, перекодирует в wav
    Переводит голосовое сообщение в текст
    Передает текст в функцию main из main.py
    '''
    
    file_info = bot.get_file(message.voice.file_id)
    voice_url = f"https://api.telegram.org/file/bot{TOKEN}/{file_info.file_path}"  # Получаем ссылку на голосовое
    file = get(voice_url)  # Скачиваем

    with open(f"voice/{message.chat.id}/file.oga", "wb") as f:
        f.write(file.content)  # Тут тоже скачиваем

    file_oga = f"voice/{message.chat.id}/file.oga"
    file_wav = f"voice/{message.chat.id}/file.wav"

    process = run(["ffmpeg", "-y", "-i", file_oga, file_wav])  # Перекодируем в нужный формат

    with sr.AudioFile(file_wav) as source:
        recog = sr.Recognizer()
        audio = recog.record(source, duration=5)    # duration - уровень подавления шума

    try:
        message.text = recog.recognize_google(audio, language="ru-RU").lower()
        if message.chat.id > 0:
            bot.send_message(message.chat.id, f"🗣 Вы сказали: {message.text.capitalize()}", parse_mode="Markdown")
    except:
        message.text = "None"


def weather(message, bot):
    bot.send_message(message.chat.id, 'Re')
