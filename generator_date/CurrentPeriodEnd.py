import calendar

from date_sling import date_sling
from params_input import given_year, link_json_last_weekend_date,link_json_weekend_date
from parser_json import pars_json
def CurrentPeriodEnd(month):
    # прибавить нолик к мксяцу если он меньше 10 числа чтобы было 01 02 03 (2025-06-01)и т.д
    if month < 10:
        new_month = str(0) + str(month)
    else:
        new_month = str(month)
    date_report = str(given_year) + '-' + str(new_month)
    last_day = calendar.monthrange(given_year, month)[1]
    date_report = date_report + '-' + str(last_day)
    txt = "последний календарный день"
    data = {"date_report": date_report, "CurrentPeriodEnd": date_report}

    return data

