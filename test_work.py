import json
from datetime import datetime
import re

def censor(info):
    info =re.split('\s+',info) # разбиение info  согласно пробелам
    if len(info[len(info)-1]) == 16: # счет или карта 
        info[len(info)-1] = re.sub(r'(\d{4})(\d\d)\d{6}(\d{4})', # (XXXX)(XX)XXXXXX(XXXX) ->
                                    r'\1 \2** **** \3', info[len(info)-1]) # XXXX XX** **** XXXX
    else:
        info[len(info)-1] = '**' + info[len(info)-1][16:] # X{20} -> **XXXX
    info = ' '.join(info) # объединение
    return info 


with open('operations.json', encoding='utf-8') as f: # чтение файла json
    dates = json.loads(f.read())
dates = [transfer for transfer in dates if transfer ] # сортировка по дате
sorted_dates = sorted(dates, key=lambda x:x.get('date') , reverse = True) 
i = 0 # счетчик 
for row in sorted_dates:
    if row.get('state') != "EXECUTED": # проверка статуса 
        continue
    i += 1 # счетчик 
    dates = datetime.strptime(row.get('date'),
                "%Y-%m-%dT%H:%M:%S.%f").strftime("%d.%m.%Y")# Форматирование даты
    if row.get('from') == None: #проверка поля from на пустоту
        froms = ''
    else:
        froms = censor(row.get('from')) + " -> "
    #вывод
    print("{} {}\n{}{}\n{} {}\n".\
    format(dates, row.get('description'),
    froms,censor(row.get('to')),row['operationAmount'].get('amount'),
    row['operationAmount']['currency'].get('name')))
    if i == 5:# проверка на вывод ровно пяти операций
        break