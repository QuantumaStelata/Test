# Функция для удаления определенных записей, которые выберет пользователь
# Запускается во второй поток каждый раз когда пользователь вызывает Удаление Элемента

import telebot
import json
import const
import re
from datetime import datetime

def delet(id, message):
    index = int(re.search(r'\d+', message.text).group()) - 1
    with open('base.json', 'r', encoding="utf-8") as f:  
        copy_base = json.loads(f.read())[str(id)] # Обход KeyError в цикле ниже
    
    i = 0 # Счетчик индекса
    IsDelete = False
    Values = True

    for key in copy_base["Work"]:
        if i == index:
            del const.copy[str(id)]["Work"][key]
            IsDelete = True
        if not const.copy[str(id)]["Work"]:
            Values = False
            break

        i += 1

    if IsDelete:
        if not Values:
            const.bot.edit_message_text(chat_id=message.chat.id, message_id=const.copy[str(message.chat.id)]["List"] + 1, text='У тебя нет дел 😔')
        else:
            new_text = '📅 Список твоих дел:\n\n'
            listcopy = sorted(const.copy[str(message.chat.id)]["Work"])

            n = 1
            for j in listcopy:
                new_text = new_text + str(n) + ') ' + j.split(' ')[0][8:10] + '.' +j.split(' ')[0][5:7] + '.' +j.split(' ')[0][0:4] + ' в '+ j.split(' ')[1][:-3] + ' - ' + const.copy[str(message.chat.id)]["Work"][j] + '\n'
                n += 1
            new_text = new_text + '\nЧтобы удалить пункт напиши - "Удалить (номер пункта)"'
            const.bot.edit_message_text(chat_id=message.chat.id, message_id=const.copy[str(message.chat.id)]["List"] + 1, text=new_text)

        with open('base.json', 'w', encoding="utf-8") as ff:
            json.dump(const.copy, ff, sort_keys=True, indent=4, ensure_ascii=False)
                        
        const.bot.send_message(id, '❌ Я удалил твою заметку')
    else:
        const.bot.send_message(id, '❔ Такой заметки нет в списке')

    
      
    
