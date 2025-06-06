import calendar
import datetime

from date_sling import date_sling
from params_input import given_year, link_json_last_weekend_date,link_json_weekend_date
from parser_json import pars_json
def startRepYear(month):
    if month < 10:
        new_month = str(0) + str(month)
    else:
        new_month = str(month)
    date_report = str(given_year) + '-' + str(new_month)
    last_day = calendar.monthrange(given_year, month)[1]
    date_report = date_report + '-' + str(last_day)

    new_year = given_year - 1
    month =12
    startRepYear = datetime.date(new_year, month, calendar.monthrange(new_year, month)[1]).strftime('%Y-%m-%d')

    data = {"date_report": date_report, "startRepYear": startRepYear}
    return data
