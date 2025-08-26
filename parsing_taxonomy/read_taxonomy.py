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
            # print("Подпапки в 'taxonomy':", subfolders)

            # получаем путь к папке nso
            path_market = f'{subfolders[0]}/{path_market}'  # без лишнего слэша в начале
            base_dir = os.path.abspath(folder_path)  # получаем абсолютный путь к 'taxonomy'
            # проверяем каждый рынок из переменной market_segments
            for segment in market_segments:

               full_segment_path = os.path.join(base_dir, path_market, segment)
               # Получаем список точек входа и их компоненты по формам
               entry_points_forms  = await entry_point(full_segment_path)
               # Получаем список точек входа и форм + периоды
               entry_points_forms_period = await get_period_from_rend(entry_points_forms,full_segment_path)

               print("Файлы в папке 'ep' (без расширения):", entry_points_forms)


        else:
            print(f"Папка '{folder_path}' не существует.")



    except Exception as e:
        # Выводим номер строки и сообщение об ошибке
        tb = traceback.format_exc()
        print(f"Ошибка произошла:\n{tb}")

# Функция перебора точек входа
async def entry_point(full_segment_path):
    entry_point = {}
    period_values_by_file = {}  # Новый словарь для хранения значений из -rend.xml

    if os.path.exists(full_segment_path) and os.path.isdir(full_segment_path):
        for root, dirs, files in os.walk(full_segment_path):
            if "ep" in os.path.basename(root).lower():
                for f in files:

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

                            # for root2, dirs, files2 in os.walk(full_segment_path):
                            #     if "tab" in os.path.basename(root2).lower():
                            #         path_tab = root2.removesuffix("tab")
                            #         # Вызов новой функции для получения значения из -rend.xml
                            #         period_value = await get_period_from_rend(path_tab, entry_point)
                            #         period_values_by_file[f] = period_value

                        except ET.ParseError:
                            print(f"Ошибка парсинга XML: {file_path}")
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

                                    formula_instant_values = await formula_instant(key_entry_point,absolute_paths, entry_points_forms)

                                    if 'new_object' not in locals():
                                        new_object = formula_instant_values  # Первый запуск: присвоение значения
                                    else:
                                        if formula_instant_values != new_object:
                                            new_object.update(formula_instant_values)
                                            print("Значения отличаются")
                            print(new_object)

                        except ET.ParseError as e:
                            print(f"Ошибка парсинга XML в файле {rend_path}: {e}")
                return new_object


# обработка  <formula:period> <formula:instant value="$par:refPeriodEnd"/>  </formula:period>
async def formula_instant (key_entry_point, absolute_paths,entry_points_forms):
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
                instant_element = period_element.xpath("./*[local-name()='instant']")
                for instant in instant_element:
                    value = instant.get('value')
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

