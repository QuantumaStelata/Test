import telebot
import sqlite3

import speech_recognition as sr
from requests import get
from subprocess import run

from const import PUSH, BASE, TABLE, NOT_PREMIUM, TOKEN, APPID, EMOJI
from log.logger import logging


def push(bot):
    '''
    Функция для рассылки сообщений пользователям
    '''
    
    push = PUSH
    if push:
        with sqlite3.connect("base.db") as db:
            cur = db.cursor()
            cur.execute(f"""SELECT chatid FROM {TABLE}""")
            for users in cur.fetchall():
                try:
                    bot.send_message(users[0], push, parse_mode="Markdown")
                    logging.info(f"{users[0]:14} | Рассылка пришла пользователю ")
                except:
                    pass


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
    '''
    Отправляет погоду по геолокации
    '''

    with sqlite3.connect(BASE) as db:
        cur = db.cursor()
        cur.execute(f"""SELECT lon, lat FROM {TABLE} WHERE chatid = {message.chat.id}""")

        geo = cur.fetchall()[0]

        res = get("http://api.openweathermap.org/data/2.5/weather",
                        params={'lat': geo[1], 'lon': geo[0], 'units': 'metric', 'lang': 'ru', 'APPID': APPID}).json()
        

        descript = res['weather'][0]['description'].capitalize()
        emoji_desc = EMOJI[res['weather'][0]['icon']]
        temp = round(res['main']['temp'])
        feels_like = round(res['main']['feels_like'])
        humidity = round(res['main']['humidity'])
        wind_speed = round(res['wind']['speed'])
        
        text_weather = f"Погода по вашей геолокации:\n\n{emoji_desc}  {descript}\n\n🌡️ Температура воздуха {temp}°\n👌 Чувствуется как {feels_like}°\n\n💦 Влажность {humidity}%\n\n🌪 Ветер {wind_speed} м/с"
        
        bot.send_message(message.chat.id, text_weather)
        
