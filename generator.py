# получаем последний рабочий день для refPeriodEnd
import calendar
import os

from generator_date.CurrentPeriodEnd import CurrentPeriodEnd
from generator_date.CurrentPeriodStart import CurrentPeriodStart
from generator_date.refPeriodEnd import refPeriodEnd
from generator_date.refPeriodStart import refPeriodStart
from generator_date.startRepYear import startRepYear
from params_input import given_year, file_path, taxonomy, entries, data_object, Entry
from parser_json import pars_json

def generator():
    for month in range(1, 13):
        # идем в обьект
        entry_point(month)


def write_path(data):

    try:
        with open(os.path.join(file_path, 'настройка рабочих дат.conf'), 'a') as file:
            file.write(
                f"{taxonomy}|{data['entry_point']}|{data['date_report']}|{data['name_parametr_ref']}|{data['work_date']}\n")
    except Exception as e:
        print(f"Ошибка при открытии файла: {e}")


def entry_point (month):
    # создан класс и перебираем в нем обьекты
    for entry in data_object:
        #получем обьект
        obj = Entry(*entry)
        # print(f"Entry(entry_point={obj.entry_point}, period={obj.period}, refPeriodEnd={obj.refPeriodEnd}, refPeriodStart={obj.refPeriodStart}, CurrentPeriodEnd={obj.CurrentPeriodEnd}, CurrentPeriodStart={obj.CurrentPeriodStart}, startRepYear={obj.startRepYear}, startQuart={obj.startQuart})")
        # Если в обьекте точка входа приравнивается к месячной

        if 'month_obj' in obj.period:
            if month in [1, 2, 4, 5, 7, 8, 10, 11]:
                for key, value in obj.__dict__.items():

                    if key == 'refPeriodStart' and value is None:
                        continue
                    if key == 'refPeriodEnd' and value is None:
                        continue
                    if key == 'CurrentPeriodStart' and value is None:
                        continue
                    if key == 'CurrentPeriodEnd' and value is None:
                        continue
                    if key == 'startRepYear' and value is None:
                        continue
                    if key == 'startQuart' and value is None:
                        continue

                    if key == 'refPeriodStart':
                        data = refPeriodStart(month)
                        obj.refPeriodStart = data['refPeriodStart']
                        entry_point = obj.entry_point
                        refPeriodStart_date = obj.refPeriodStart
                        data = {'entry_point': entry_point, "date_report": data['date_report'], 'name_parametr_ref':'$par:refPeriodStart','work_date': refPeriodStart_date}
                        write_path(data)

                    if key == 'refPeriodEnd':
                        data = refPeriodEnd(month)
                        obj.refPeriodEnd = data['refPeriodEnd']
                        entry_point = obj.entry_point
                        refPeriodEnd_date = obj.refPeriodEnd
                        data = {'entry_point': entry_point, "date_report": data['date_report'],
                                'name_parametr_ref': '$par:refPeriodEnd', 'work_date': refPeriodEnd_date}
                        write_path(data)

                    if key == 'CurrentPeriodStart':
                        data = CurrentPeriodStart(month)
                        obj.CurrentPeriodStart = data['CurrentPeriodStart']
                        entry_point = obj.entry_point
                        CurrentPeriodStart_date = obj.CurrentPeriodStart
                        data = {'entry_point': entry_point, "date_report": data['date_report'],
                                'name_parametr_ref': '$par:CurrentPeriodStart', 'work_date': CurrentPeriodStart_date}
                        write_path(data)


                    if key == 'CurrentPeriodEnd':
                        data = CurrentPeriodEnd(month)
                        obj.CurrentPeriodEnd = data['CurrentPeriodEnd']
                        entry_point = obj.entry_point
                        CurrentPeriodEnd_date = obj.CurrentPeriodEnd
                        data = {'entry_point': entry_point, "date_report": data['date_report'],
                                'name_parametr_ref': '$par:CurrentPeriodEnd', 'work_date': CurrentPeriodEnd_date}
                        write_path(data)
            # print(f"Entry(entry_point={obj.entry_point}, period={obj.period}, refPeriodEnd={obj.refPeriodEnd}, refPeriodStart={obj.refPeriodStart}, CurrentPeriodEnd={obj.CurrentPeriodEnd}, CurrentPeriodStart={obj.CurrentPeriodStart}, startRepYear={obj.startRepYear}, startQuart={obj.startQuart})")
