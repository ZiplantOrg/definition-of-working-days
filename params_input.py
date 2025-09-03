from importlib.metadata import entry_points

from my_dictionary import my_dictionary

# входные данные:
# директория для сохранения настроек рабочих дат
file_path = "/home/vlad/Документы/Vlad/definition-of-working-days/weekend_date"

# cайт откуда я взял выходные дни
#link = https://xmlcalendar.ru/index.php?country=ru

# текущий год только выходных дней (можно поменять год)
# link_json_weekend_date = 'https://xmlcalendar.ru/data/ru/2025/calendar.json'

# Если отсутсвует ссылка на новыф год можно переключить на свой справлчник
link_json_weekend_date =  my_dictionary()


# предыдущий год только выходных дней (можно поменять год)
link_json_last_weekend_date = 'https://xmlcalendar.ru/data/ru/2025/calendar.json'


# текущий год
given_year = 2026
# текущая версия таксономии
taxonomy = 7.1

# Создание списка точек входа для автоматического построеня параметров дат в точке входа.
work_entry_point = [
    ('ep_nso_uk_m_10rd'),
    ('ep_nso_uk_q_10rd'),
    ('ep_nso_uk_y_10rd'),
    ('ep_nso_aif_uk_m_10rd_specdep'),
    ('ep_nso_aif_uk_q_10rd_specdep'),
    ('ep_nso_aif_uk_y_10rd_specdep'),
    ("ep_nso_aif_uk_m_q_y_20rd")
]

# Создание списка данных 7.1 вручную(сделать список пустым, так как в файле generator условие: если список data_object пустой, то формировать даты в автоматическом варианте /
# если список заполнен то сформировать даты в ручном режиме)

# ==================ручная генерация=========================
data_object = [
        # ('ep_nso_uk_m_10rd', 'month_obj', '$par:refPeriodEnd','$par:refPeriodStart','$par:CurrentPeriodEnd','$par:CurrentPeriodStart'),
        # ('ep_nso_uk_q_10rd', 'quart_obj','$par:refPeriodEnd','$par:refPeriodStart','$par:CurrentPeriodEnd','$par:CurrentPeriodStart','$par:startQuart','$par:startRepYear',),
        # ('ep_nso_uk_y_10rd', 'year_obj','$par:refPeriodEnd','$par:refPeriodStart','$par:CurrentPeriodEnd','$par:CurrentPeriodStart','$par:startQuart','$par:startRepYear'),
        # ('ep_nso_aif_uk_m_10rd_specdep', 'month_obj','$par:refPeriodEnd','$par:refPeriodStart','$par:CurrentPeriodEnd','par:CurrentPeriodStart'),
        # ('ep_nso_aif_uk_q_10rd_specdep', 'quart_obj','$par:refPeriodEnd','$par:refPeriodStart','$par:CurrentPeriodEnd','par:CurrentPeriodStart','$par:startQuart','$par:startRepYear'),
        # ('ep_nso_aif_uk_y_10rd_specdep', 'year_obj','$par:refPeriodEnd','$par:refPeriodStart','$par:CurrentPeriodEnd','par:CurrentPeriodStart','$par:startQuart','$par:startRepYear'),
        # ('ep_nso_aif_uk_m_q_y_20rd', 'month_obj','$par:refPeriodEnd','$par:refPeriodStart','$par:CurrentPeriodEnd','$par:CurrentPeriodStart'),
        # ('ep_nso_aif_uk_m_q_y_20rd', 'quart_obj','$par:refPeriodEnd','$par:refPeriodStart','$par:CurrentPeriodEnd','$par:CurrentPeriodStart'),
        # ('ep_nso_aif_uk_m_q_y_20rd', 'year_obj','$par:refPeriodEnd','$par:refPeriodStart','$par:CurrentPeriodEnd','$par:CurrentPeriodStart'),
        ]

# Создание списка данных 6.1
# data_object = [
#         ('ep_nso_uk_m_10rd', 'month_obj', '$par:refPeriodEnd','$par:refPeriodStart','$par:CurrentPeriodEnd','$par:CurrentPeriodStart'),
#         ('ep_nso_uk_q_y_10rd', 'quart_obj','$par:refPeriodEnd','$par:refPeriodStart','$par:CurrentPeriodEnd','$par:CurrentPeriodStart','$par:startQuart','$par:startRepYear',),
#         ('ep_nso_uk_q_y_10rd', 'year_obj','$par:refPeriodEnd','$par:refPeriodStart','$par:CurrentPeriodEnd','$par:CurrentPeriodStart','$par:startQuart','$par:startRepYear'),
#         ('ep_nso_aif_uk_m_10rd_specdep', 'month_obj','$par:refPeriodEnd','$par:refPeriodStart','$par:CurrentPeriodEnd'),
#         ('ep_nso_aif_uk_q_y_10rd_specdep', 'quart_obj','$par:refPeriodEnd','$par:refPeriodStart','$par:CurrentPeriodEnd','$par:startQuart','$par:startRepYear'),
#         ('ep_nso_aif_uk_q_y_10rd_specdep', 'year_obj','$par:refPeriodEnd','$par:refPeriodStart','$par:CurrentPeriodEnd','$par:startQuart','$par:startRepYear'),
#         ('ep_nso_aif_uk_m_q_y_20rd', 'month_obj','$par:refPeriodEnd','$par:refPeriodStart','$par:CurrentPeriodEnd'),
#         ('ep_nso_aif_uk_m_q_y_20rd', 'quart_obj','$par:refPeriodEnd','$par:refPeriodStart','$par:CurrentPeriodEnd'),
#         ('ep_nso_aif_uk_m_q_y_20rd', 'year_obj','$par:refPeriodEnd','$par:refPeriodStart','$par:CurrentPeriodEnd'),
#         ]

# Создание класса
class Entry:
    def __init__(self, entry_point=None, period=None, refPeriodEnd=None, refPeriodStart=None, CurrentPeriodEnd=None, CurrentPeriodStart=None, startQuart=None,startRepYear=None):
        self.entry_point = entry_point
        self.period = period
        self.refPeriodEnd = refPeriodEnd
        self.refPeriodStart = refPeriodStart
        self.CurrentPeriodEnd = CurrentPeriodEnd
        self.CurrentPeriodStart = CurrentPeriodStart
        self.startQuart = startQuart
        self.startRepYear = startRepYear

# Создание множества объектов
entries = [Entry(*entry) for entry in data_object]


