# Принимает голосовое сообщение
# Скачивает, перекодирует в wav
# Распознает голос

import telebot
import speech_recognition as sr
from requests import get
from subprocess import run

from const import TOKEN


def voice(message, bot):
    file_info = bot.get_file(message.voice.file_id)
    voice_url = "https://api.telegram.org/file/bot{0}/{1}".format(TOKEN, file_info.file_path)  # Получаем ссылку на голосовое
    file = get(voice_url)  # Скачиваем

    with open("voice/{}/file.oga".format(str(message.chat.id)), "wb") as f:
        f.write(file.content)  # Тут тоже скачиваем

    file_oga = "voice/{}/file.oga".format(str(message.chat.id))
    file_wav = "voice/{}/file.wav".format(str(message.chat.id))

    process = run(["ffmpeg", "-y", "-i", file_oga, file_wav])  # Перекодируем в нужный формат

    with sr.AudioFile(file_wav) as source:
        recog = sr.Recognizer()
        audio = recog.record(source, duration=5)

    try:
        message.text = recog.recognize_google(audio, language="ru-RU").lower()
        if message.chat.id > 0:
            bot.send_message(message.chat.id, "🗣 Вы сказали: " + message.text.capitalize(), parse_mode="Markdown")
    except:
        message.text = "None"