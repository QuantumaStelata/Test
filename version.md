﻿# telebot

Бот-напоминалка для летней практики 2020. Работает на базе Telegram.

Альфа-Тест:
    Добавили:
        1) Основной функционал

Бета-тест:
    Добавили:
        1) TimeZone
        2) Поменяли структуру базы данных с {'ChatId': {'Time': 'Text'}} на {'ChatId': {'TZ': {'Time': 'Text'}}}
        3) Функцию callback для связи с разработчиком

Версия 0.1:
    Добавили:
        1) Поменяли структуру базы данных с {'ChatId': {'TZ': {'Time': 'Text'}}} на {'ChatId': {'1Name': 'Name', '2Name': 'Name' и т.д.}}
        2) Добавили функцию reguser
        3) Оптимизировали обработку запросов. Уменьшили ожидание с 0.7-0.8 секунд до 0.3-0.4 секунд (в среднем)
        4) Решена проблема с удалением заметок в базе

Версия 0.2:
    Добавили:
        1) Создан репозиторий на GitHub
        2) Добавили функцию voice. Добавили обработку голосовых сообщений
        3) Добавили пунк "Voice" в БД.
        4) Улучшили распознавание сообщений от пользователя

Версия 0.3:
    Добавили:
        1) Меняем базу с json на SQLite3.
        2) Оптимизировали re для inminute.py
        3) Оптимизировали re для inhour.py
        4) Оптимизировали re для athour.py
        5) Оптимизировали re для atdate.py
        6) Добавили sticker.py. Добавили обработку стикеров

Версия 0.4:
    Добавили:
        1) В базу добавлено поле "premium" для обозначения премиум аккаунта
        2) Вынесли функцию команды /list из main в list_.py
        3) Провели оптимизацию, добавив f-строки
        4) Пофиксили баг с ID стикеров
        5) Собрали функции в файлы content_message_*

Версия 0.5:
    Добавили:
        1) Добавили lon, lat в базе у пользователе
        2) Сделали регистрацию по геолокации
        3) Часовой пояс определяется по геолокации
        4) Команда /weather показывает погоду по геолокации