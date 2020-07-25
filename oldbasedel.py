# Функция для удаления устаревших записей пользователей
# Запускается в main первая и один раз

import json
import const
from datetime import datetime, timedelta

def old_base_del():
    with open('base.json', 'r', encoding="utf-8") as f:  
        copy_base = json.loads(f.read()) # Обход KeyError в цикле ниже

    for key in copy_base:
        for key1, val1 in copy_base[key]["Work"].items():
            now = datetime.now() + timedelta(hours = int(copy_base[key]['TZ']))
            data = datetime(int(key1[0:4]), int(key1[5:7]), int(key1[8:10]), int(key1[11:13]), int(key1[14:16]), int(key1[17:19]))
            if now > data:
                del const.copy[key]['Work'][key1]

                with open('base.json', 'w', encoding="utf-8") as ff:
                        json.dump(const.copy, ff, sort_keys=True, indent=4, ensure_ascii=False)
    
