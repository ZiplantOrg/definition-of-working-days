

def date_sling(data):
    parametr_date = data['parametr_date']
    year = data['year']
    month = data['month']
    last_day = data['last_day']
    txt = data['txt']
    date_report = data['date_report']

    if month < 10: month = str(0) + str(month)
    date = str(year) + '-' + str(month) + '-' + str(last_day)
    print(f"{date}|{txt}")

    return date
