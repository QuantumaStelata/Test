import speech_recognition as sr
import os
import sys
import webbrowser
import pyttsx3
import pyglet
import requests
import subprocess
#from pydub import AudioSegment
import time
#def talk(words):
#    print(words)
#    engine = pyttsx3.init()
#    engine.say(words)
#    engine.runAndWait()
#
#talk("Привет, спроси у меня что-либо")

def command():
    start_time = time.time()
    r = sr.Recognizer()
    
    file = requests.get('https://api.telegram.org/file/bot889111380:AAHigT0L4olDY780-FmImJjYPJb-JHqdlFs/voice/file_30.oga')
    
    

    with open('file.oga','wb') as b:
        b.write(file.content)

    src_filename = 'file.oga'
    dest_filename = 'file.wav'

    process = subprocess.run(['ffmpeg', '-i', src_filename, dest_filename]) 
    
    
    sample_audio = sr.AudioFile('file.wav')
    
    with sample_audio as source:
       
        recog = sr.Recognizer() 
        audio = recog.record(source, duration=10)
    
    zadanie = r.recognize_google(audio, language="ru-RU").lower()
    print("Вы сказали " +  zadanie)
    
    print("--- %s seconds ---" % (time.time() - start_time))
    

command()