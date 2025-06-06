import calendar
import datetime

from date_sling import date_sling
from params_input import given_year, link_json_last_weekend_date,link_json_weekend_date
from parser_json import pars_json
from dateutil.relativedelta import relativedelta

def startQuart(month, new_year=None):
    if month < 10:
        new_month = str(0) + str(month)
    else:
        new_month = str(month)
    date_report = str(given_year) + '-' + str(new_month)
    last_day = calendar.monthrange(given_year, month)[1]
    date_report = date_report + '-' + str(last_day)

    given_quarter_day = datetime.date(given_year, month, calendar.monthrange(given_year, month)[1]).strftime('%Y-%m-%d')
    # предположим, что given_quarter_day уже определен
    given_quarter_day = datetime.datetime.strptime(given_quarter_day, '%Y-%m-%d')

    # вычитаем 3 месяца
    given_quarter_day = given_quarter_day - relativedelta(months=3)

    # получаем последний день месяца
    last_day_of_month = calendar.monthrange(given_quarter_day.year, given_quarter_day.month)[1]

    # устанавливаем день в полученное значение
    given_quarter_day = given_quarter_day.replace(day=last_day_of_month)

    # преобразуем обратно в строку
    given_quarter_day = given_quarter_day.strftime('%Y-%m-%d')

    txt = "последний календарный день"
    data = {"date_report": date_report, "startQuart": given_quarter_day}
    return data