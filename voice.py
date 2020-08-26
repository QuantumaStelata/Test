# Принимает голосовое сообщение
# Скачивает, перекодирует в wav
# Переводит голосовое сообщение в текст
# Передает текст в функцию main из main.py

import telebot
import speech_recognition as sr
from requests import get
from subprocess import run

from const import TOKEN


def voice(message, bot):
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
        audio = recog.record(source, duration=5)

    try:
        message.text = recog.recognize_google(audio, language="ru-RU").lower()
        if message.chat.id > 0:
            bot.send_message(message.chat.id, f"🗣 Вы сказали: {message.text.capitalize()}", parse_mode="Markdown")
    except:
        message.text = "None"