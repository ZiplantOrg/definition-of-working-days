from importlib.metadata import entry_points

file_path = "/home/vlad/Документы/Vlad/definition-of-working-days/weekend_date" # директопия соранения настроек рабочих дат
#link = https://xmlcalendar.ru/index.php?country=ru
link_json_weekend_date = 'https://xmlcalendar.ru/data/ru/2025/calendar.json' # текущий год только выходных дней
link_json_last_weekend_date = 'https://xmlcalendar.ru/data/ru/2024/calendar.json' # предыдущий год только выходных дней
given_year = 2025 # текущий год
taxonomy = 6.1  # текущая версия таксономии



# Создание списка данных
data_object = [
        ('ep_nso_uk_m_10rd', 'month_obj', '$par:refPeriodEnd','$par:refPeriodStart','$par:CurrentPeriodEnd','$par:CurrentPeriodStart'),
        ('ep_nso_uk_q_y_10rd', 'quart_obj','$par:startRepYear','$par:startQuart','$par:refPeriodEnd','$par:refPeriodStart','$par:CurrentPeriodEnd','$par:CurrentPeriodStart'),
        ('ep_nso_uk_q_y_10rd', 'year_obj','$par:startRepYear','$par:startQuart','$par:refPeriodEnd','$par:refPeriodStart','$par:CurrentPeriodEnd','$par:CurrentPeriodStart'),
        ]


# Создание класса
class Entry:
    def __init__(self, entry_point=None, period=None, refPeriodEnd=None, refPeriodStart=None, CurrentPeriodEnd=None, CurrentPeriodStart=None, startRepYear=None, startQuart=None):
        self.entry_point = entry_point
        self.period = period
        self.refPeriodEnd = refPeriodEnd
        self.refPeriodStart = refPeriodStart
        self.CurrentPeriodEnd = CurrentPeriodEnd
        self.CurrentPeriodStart = CurrentPeriodStart
        self.startRepYear = startRepYear
        self.startQuart = startQuart

# Создание множества объектов
entries = [Entry(*entry) for entry in data_object]





# ('ep_nso_aif_uk_q_y_10rd_specdep', 'quart')
# ('ep_nso_aif_uk_q_y_10rd_specdep', 'year')
#
# ('ep_nso_aif_uk_m_q_y_20rd', 'month')
# ('ep_nso_aif_uk_m_q_y_20rd', 'quart')
# ('ep_nso_aif_uk_m_q_y_20rd', 'year')
#
# ('ep_nso_aif_uk_q_y_10rd_specdep', 'quart')
# ('ep_nso_aif_uk_q_y_10rd_specdep', 'year')
# ('ep_nso_aif_uk_m_10rd_specdep', 'month')