import calendar

from params_input import given_year, link_json_last_weekend_date,link_json_weekend_date
from parser_json import pars_json
def refCurrentPeriodStart(month):
    if month == 1:
      new_year = given_year -1
      month =12
    else:
        new_year = given_year
        month = month - 1
    last_day = calendar.monthrange(new_year, month)[1]
    txt = "последний календарный день"
    return {'parametr_date': "refCurrentPeriodStart", 'year': new_year, 'month': month, 'last_day': last_day, 'txt': txt}

