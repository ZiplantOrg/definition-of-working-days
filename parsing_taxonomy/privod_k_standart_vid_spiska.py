import traceback

async def privod_k_standart_vid_spiska(result):
    try:

        data_object = []

        for key, value in result.items():
            # Удаление расширения .xsd из ключа
            base_key = key.split('.')[0]

            # Извлечение параметров, исключая 'key_period'
            params = [v for k, v in value.items() if k.startswith('$par')]

            # Добавление типа периода (month_obj, quart_obj, year_obj)
            params.append(value['key_period'])

            # Формирование кортежа в формате (base_key, ...) + params
            data_object.append((base_key,) + tuple(params))

        # Результирующий список
        print('преобразовали в список',data_object)
        return data_object

    except Exception as e:
        tb = traceback.format_exc()
        print(f"Ошибка произошла:\n{tb}")