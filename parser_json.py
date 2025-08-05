import requests
import json
from params_input import link_json_weekend_date

def pars_json(year_pars):
    x = 0  # инициализируем счётчик

    # Загружаем JSON из URL
    try:
        response = requests.get(year_pars)
        # Преобразуем ответ в JSON
        data = response.json()
    except Exception as e:
        print(f"Ошибка при получении JSON: {e}")
        data = year_pars  # увеличиваем счётчик при ошибке

    # Выводим JSON на экран
    # print(json.dumps(data, indent=4))
    return data
