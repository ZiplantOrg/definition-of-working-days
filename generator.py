# получаем последний рабочий день для refPeriodEnd
import calendar
import os

from generator_date.refCurrentPeriodStart import refCurrentPeriodStart
from generator_date.refPeriodEnd import refPeriodEnd
from generator_date.refPeriodStart import refPeriodStart
from params_input import given_year, file_path
from parser_json import pars_json

def generator():
    for month in range(1, 13):

        #модули_________
        data = refPeriodEnd(month)
        write_path(data)
        data = refPeriodStart(month)
        write_path(data)
        data = refCurrentPeriodStart(month)
        write_path(data)


def write_path(data):
    parametr_date = data['parametr_date']
    year = data['year']
    month = data['month']
    last_day = data['last_day']
    txt = data['txt']

    if month <10:month = str(0) + str(month)
    date = str(year) + '-' + str(month) + '-' + str(last_day)
    print(f"{date}|{txt}")
    try:
        with open(os.path.join(file_path, 'настройка рабочих дат.conf'), 'a') as file:
            file.write(f"$par:{parametr_date}|{date}|{txt} \n")
    except Exception as e:
        print(f"Ошибка при открытии файла: {e}")