# получаем последний рабочий день для refPeriodEnd
import calendar
import os

from generator_date.refPeriodEnd import refPeriodEnd
from params_input import year, file_path
from parser_json import pars_json

def generator():
    for month in range(1, 13):
            last_day = calendar.monthrange(year, month)[1]
            # print(f"Последний день {month} месяца: {last_day}")
            # получить список выходных дней
            weekend_date = pars_json()
            # получить список выходных по каждому месяцу
            weekend_days = [int(day.replace('+', '')) for day in weekend_date['months'][month - 1]['days'].split(',') if
                            '*' not in day]
            #модули_________
            data = refPeriodEnd(last_day,weekend_days,month)
            write_path(data)



def write_path(data):
    month = data['month']
    last_day = data['last_day']
    txt = data['txt']

    if month <10:month = str(0) + str(month)
    date = str(year) + '-' + str(month) + '-' + str(last_day)
    print(f"{date} {txt}")
    try:
        with open(os.path.join(file_path, 'настройка рабочих дат.conf'), 'a') as file:
            file.write(f"$par:refPeriodEnd|{date}  {txt} \n")
    except Exception as e:
        print(f"Ошибка при открытии файла: {e}")