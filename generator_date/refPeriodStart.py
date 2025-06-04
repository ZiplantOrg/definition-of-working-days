import calendar

from params_input import given_year, link_json_last_weekend_date,link_json_weekend_date
from parser_json import pars_json


def refPeriodStart(month):
    if month < 10:
        new_month = str(0) + str(month)
    else:
        new_month = str(month)
    date_report =  str(given_year) + '-' + str(new_month)
    last_day = calendar.monthrange(given_year, month)[1]
    date_report = date_report + '-' + str(last_day)

    if month == 1:
      new_year = given_year -1
      month =12
      year_pars = link_json_last_weekend_date
    else:
        year_pars = link_json_weekend_date
        new_year = given_year
        month = month - 1
        year_pars = link_json_weekend_date
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
                txt =  "предыдущий календарный рабочий день Является выходным днем и делам -1 день"

                return {'date_report':date_report,'parametr_date': "refPeriodStart",'year':new_year,'month': month, 'last_day': last_day, 'txt': txt}
                break
    else:
        txt = "предыдущий календарный рабочий день Не является выходным днем"
        return {'date_report':date_report,'parametr_date': "refPeriodStart",'year': new_year, 'month': month, 'last_day': last_day, 'txt': txt}