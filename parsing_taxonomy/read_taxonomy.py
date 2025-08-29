import os
import traceback
import xml.etree.ElementTree as ET
from xml import etree

from lxml import etree as ET
from pathlib import Path

async def read_taxonomy():
    folder_path = 'taxonomy'
    path_market = 'www.cbr.ru/xbrl/nso/'
    market_segments = {'uk', 'srki'}

    try:
        # Проверяем, существует ли папка taxonomy
        if os.path.exists(folder_path) and os.path.isdir(folder_path):

            # Получаем список всех подпапок
            subfolders = [f.name for f in os.scandir(folder_path) if f.is_dir()]

            # получаем путь к папке nso
            path_market = f'{subfolders[0]}/{path_market}'  # без лишнего слэша в начале

            # получаем абсолютный путь к 'taxonomy'
            base_dir = os.path.abspath(folder_path)

            # Инициализация пустого словаря
            entry_points_all_segment_forms_period = {}

            # прорабатываем каждый рынок из переменной market_segments присваимем периоды которые находятся в каждой точке входа
            for segment in market_segments:
               # получаем путь к сегменту рынка
               full_segment_path = os.path.join(base_dir, path_market, segment)

               # Получаем список точек входа и их компоненты по формам
               entry_points_forms  = await entry_point(full_segment_path)

               # Получаем список точек входа и форм + периоды
               entry_points_one_segment_forms_period = await get_period_from_rend(entry_points_forms,full_segment_path)
               # Обновляем список с точками входа
               entry_points_all_segment_forms_period.update(entry_points_one_segment_forms_period)

            # присвоить маркеры month_obj/quart_obj/year_obj
            entry_points_all_segment_forms_period =  await period_marker(entry_points_all_segment_forms_period)
            print("точка входа период:", entry_points_all_segment_forms_period)

        else:
            print(f"Папка '{folder_path}' не существует.")



    except Exception as e:
        # Выводим номер строки и сообщение об ошибке
        tb = traceback.format_exc()
        print(f"Ошибка произошла:\n{tb}")

# Функция перебора точек входа
async def entry_point(full_segment_path):
    # Инцилизация списка
    entry_point = {}

    if os.path.exists(full_segment_path) and os.path.isdir(full_segment_path):
        for root, dirs, files in os.walk(full_segment_path):
            if "ep" in os.path.basename(root).lower():
                for f in files:
                    # получаем список точек входа в сегменте рынка
                    file_path = os.path.join(root, f)
                    if f.endswith('.xsd'):
                        try:
                            tree = ET.parse(file_path)
                            root_xml = tree.getroot()

                            schema_locations = [
                                elem.get("schemaLocation")
                                for elem in root_xml.xpath(
                                    ".//xs:import", namespaces={"xs": "http://www.w3.org/2001/XMLSchema"}
                                )
                                if elem.get("schemaLocation")
                            ]
                            entry_point[f] = schema_locations
                            # Добавляем фильтрацию и сохранение только путей, начинающихся с '../tab'
                            tab_paths = [path for path in schema_locations if path.startswith('../tab')]
                            entry_point[f] = tab_paths  # Сохраняем отдельно

                        except ET.ParseError:
                            print(f"Ошибка парсинга XML entry_point : {file_path}")

        return entry_point

    else:
        print(f"Папка '' не существует: {full_segment_path}")
        return {}, {}

# функция получения всех ref period в рамках одной точки входа
async def get_period_from_rend(entry_points_forms,full_segment_path):
    if os.path.exists(full_segment_path) and os.path.isdir(full_segment_path):
        for root, dirs, files in os.walk(full_segment_path):
            if "tab" in os.path.basename(root).lower():
                path_tab = root.removesuffix("tab")
                for key_entry_point, value_list in entry_points_forms.items():
                    print(f"Ключ: {key_entry_point}")
                    for value in value_list:
                        clean_value = value.replace('../', '', 1)
                        rend_path = path_tab + '/' + clean_value

                        if not os.path.exists(rend_path):
                            return None
                        try:
                            tree = ET.parse(rend_path)
                            root = tree.getroot()

                            # Определение пространств имён (важно для корректной работы XPath)
                            namespaces = {
                                'xsd': 'http://www.w3.org/2001/XMLSchema',
                                'link': 'http://www.xbrl.org/2003/linkbase'
                            }

                            # XPath запрос для получения всех link:linkbaseRef
                            xpath_query = '//xsd:annotation/xsd:appinfo/link:linkbaseRef'

                            # Выполнение запроса
                            linkbase_refs = root.xpath(xpath_query, namespaces=namespaces)

                            # Список для хранения абсолютных путей
                            absolute_paths = []

                            # перебор форм rend внутри уже формы.
                            for ref in linkbase_refs:
                                href = ref.get('{http://www.w3.org/1999/xlink}href')
                                if href:
                                    # Объединяем путь до xsd-файла и имя файла из xlink:href

                                    # Преобразуем строку в объект Path
                                    path = Path(rend_path)
                                    # Переходим на один уровень выше
                                    parent_path = path.parent

                                    full_path = os.path.join(parent_path, href)
                                    absolute_paths.append(full_path)

                                    absolute_paths = [path for path in absolute_paths if path.endswith('-rend.xml')]
                                    # обрабатываем даты instance
                                    formula_instant_values = await formula_instant(key_entry_point,absolute_paths, entry_points_forms)

                                    if 'new_object' not in locals():
                                        new_object = formula_instant_values  # Первый запуск: присвоение значения
                                    else:
                                        if formula_instant_values != new_object:
                                            new_object.update(formula_instant_values)
                                            print("Значения отличаются")

                                    # обрабатываем даты duration
                                    formula_duration_values = await formula_duration(key_entry_point, absolute_paths, entry_points_forms)

                                    if 'new_object' not in locals():
                                        new_object = formula_duration_values  # Первый запуск: присвоение значения
                                    else:
                                        if formula_duration_values != new_object:
                                            new_object.update(formula_duration_values)
                                            print("Значения отличаются")

                        except ET.ParseError as e:
                            print(f"Ошибка парсинга XML в файле {rend_path}: {e}")
                return new_object

# обработка  <formula:period> <formula:instant value="$par:refPeriodEnd"/>  </formula:period>
async def formula_instant (key_entry_point, absolute_paths,entry_points_forms):
    values = []
    # Обрабатываем каждый файл из absolute_paths
    for file_path in absolute_paths:
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            instants = root.xpath("//*[local-name()='link']/*[local-name()='ruleNode']/*[local-name()='period']")
            # Поиск всех элементов <formula:period>
            for period_element in instants:
                # Внутри каждого <formula:period> ищем <formula:instant>
                instant_element = period_element.xpath("./*[local-name()='instant']")
                for instant in instant_element:
                    value = instant.get('value')
                    if value:
                        if not values or value not in values:  # Проверка на пустоту и дублирование
                            values.append(value)
                            # entry_name = next(iter(entry_points_forms.keys()))
                            entry_name = key_entry_point
                            # Если entry_points_forms[entry_name] ещё не является словарём, преобразуем его
                            if not isinstance(entry_points_forms[entry_name], dict):
                                entry_points_forms[entry_name] = {}
                            # Используем значение переменной key как ключ в словаре
                            key = value
                            entry_points_forms[entry_name][key] = value


        except Exception as e:
            print(f"Ошибка при обработке файла {file_path}: {e}")
    return entry_points_forms

# обработка  <formula:period> <formula:duration
async def formula_duration (key_entry_point, absolute_paths,entry_points_forms):
    key_entry_point = key_entry_point
    values = []
    # Обрабатываем каждый файл из absolute_paths
    for file_path in absolute_paths:
        try:
            tree = ET.parse(file_path)
            root = tree.getroot()
            instants = root.xpath("//*[local-name()='link']/*[local-name()='ruleNode']/*[local-name()='period']")
            # Поиск всех элементов <formula:period>
            for period_element in instants:
                # Внутри каждого <formula:period> ищем <formula:instant>
                instant_element = period_element.xpath("./*[local-name()='duration']")
                for instant in instant_element:
                    value = instant.get('start')
                    if '+' in value:
                        # Удаляем все, что идет после символа '+'
                        value = value.split('+')[0].strip()

                    if value:
                        if not values or value not in values:  # Проверка на пустоту и дублирование
                            values.append(value)
                            # entry_name = next(iter(entry_points_forms.keys()))
                            entry_name = key_entry_point
                            # Если entry_point[entry_name] ещё не является словарём, преобразуем его
                            if not isinstance(entry_points_forms[entry_name], dict):
                                entry_points_forms[entry_name] = {}
                            # Используем значение переменной key как ключ в словаре
                            key = value
                            entry_points_forms[entry_name][key] = value

        except Exception as e:
            print(f"Ошибка при обработке файла {file_path}: {e}")
    return entry_points_forms

async def period_marker(entry_points_all_segment_forms_period):
    # Создаем копию ключей, чтобы избежать изменения словаря во время итерации
    for entry_point in list(entry_points_all_segment_forms_period.keys()):
        key_period = "key_period"

        if "m" in entry_point and "q" not in entry_point and "y" not in entry_point:
            key = "month_obj"
            entry_points_all_segment_forms_period[entry_point][key_period] = key

        elif "q" in entry_point and "m" not in entry_point and "y" not in entry_point:
            key = "quart_obj"
            entry_points_all_segment_forms_period[entry_point][key_period] = key

        elif "y" in entry_point and "m" not in entry_point and "q" not in entry_point:
            key = "year_obj"
            entry_points_all_segment_forms_period[entry_point][key_period] = key

        elif "m_q_y" in entry_point:
            original = entry_points_all_segment_forms_period[entry_point].copy()

            # Дубликат 1: year_obj
            original_copy_1 = original.copy()
            original_copy_1[key_period] = "year_obj"
            entry_points_all_segment_forms_period[f"{entry_point}_year"] = original_copy_1

            # Дубликат 2: quart_obj
            original_copy_2 = original.copy()
            original_copy_2[key_period] = "quart_obj"
            entry_points_all_segment_forms_period[f"{entry_point}_quart"] = original_copy_2

            # Дубликат 3: month_obj
            original_copy_3 = original.copy()
            original_copy_3[key_period] = "month_obj"
            entry_points_all_segment_forms_period[f"{entry_point}_month"] = original_copy_3

            # Удаляем оригинальный элемент
            del entry_points_all_segment_forms_period[entry_point]
        else:
            key = "null"
            entry_points_all_segment_forms_period[entry_point][key_period] = key

    return entry_points_all_segment_forms_period


        # entry_points_forms[entry_point][key] = value
