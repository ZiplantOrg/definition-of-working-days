# получаем последний рабочий день для refPeriodEnd
import calendar
import os
from params_input import year, file_path
from parser_json import pars_json

def refPeriodStart():
    # 1. Получить календарную дату каждого месяца
    get_last_day_of_month_pred_month(year)

# 2. Получить календарную дату каждого месяца
def get_last_day_of_month_pred_month(year):
    for month in range(1, 13):
        last_day = calendar.monthrange(year, month)[1]
        # print(f"Последний день {month} месяца: {last_day}")
        # получить список выходных дней
        weekend_date = pars_json()
        # получить список выходных по каждому месяцу
        weekend_days = [int(day.replace('+', '')) for day in weekend_date['months'][month - 1]['days'].split(',') if '*' not in day]

        if last_day in weekend_days:
            while True:
                last_day -= 1
                if not last_day in  weekend_days:
                    txt =  "Является выходным днем и делам -1 день"
                    write_path(month,last_day,txt)
                    break
        else:
            txt = " Не является выходным днем"
            write_path(month,last_day,txt)



def write_path(month,last_day,txt ):
    if month <10:month = str(0) + str(month)
    date = str(year) + '-' + str(month) + '-' + str(last_day)
    print(f"{date} {txt}")
    with open(os.path.join(file_path, 'настройка рабочих дат.conf'), 'a') as file:
        file.write(f"$par:refPeriodEnd|{date}  {txt} \n")