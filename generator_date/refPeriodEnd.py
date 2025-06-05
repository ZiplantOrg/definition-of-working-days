import calendar

from date_sling import date_sling
from params_input import given_year, link_json_weekend_date
from parser_json import pars_json


def refPeriodEnd(month):
    if month < 10:
        new_month = str(0) + str(month)
    else:
        new_month = str(month)
    date_report = str(given_year) + '-' + str(new_month)

    year_pars = link_json_weekend_date
    last_day = calendar.monthrange(given_year, month)[1]
    date_report = date_report + '-' + str(last_day)
    # print(f"Последний день {month} месяца: {last_day}")
    # получить список выходных дней
    weekend_date = pars_json(year_pars)
    # получить список выходных по каждому месяцу
    weekend_days = [int(day.replace('+', '')) for day in weekend_date['months'][month - 1]['days'].split(',') if
                    '*' not in day]

    if last_day in weekend_days:
        while True:
            last_day -= 1
            if not last_day in  weekend_days:
                txt =  "Является выходным днем и делам -1 день"
                data =  {'date_report':date_report,'parametr_date': "refPeriodEnd", 'year': given_year, 'month': month, 'last_day': last_day,
                        'txt': txt}
                refPeriodEnd = date_sling(data)
                return refPeriodEnd
                break
    else:
        txt = "Не является выходным днем"
        data = {'date_report': date_report, 'parametr_date': "refPeriodEnd", 'year': given_year, 'month': month,
                'last_day': last_day,
                'txt': txt}
        refPeriodEnd = date_sling(data)
        return refPeriodEnd

