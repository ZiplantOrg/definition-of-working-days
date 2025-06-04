


# 2. Получить календарную дату каждого месяца
def refPeriodEnd(last_day,weekend_days,month):
        if last_day in weekend_days:
            while True:
                last_day -= 1
                if not last_day in  weekend_days:
                    txt =  "Является выходным днем и делам -1 день"
                    return {'month': month, 'last_day': last_day, 'txt': txt}
                    break
        else:
            txt = " Не является выходным днем"
            return {'month': month, 'last_day': last_day, 'txt': txt}

