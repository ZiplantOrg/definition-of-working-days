import traceback

from params_input import work_entry_point


async def dell_extra_entry_point(result):
    try:

        filtered_result = {
            key: value for key, value in result.items()
            if any(entry_point in key for entry_point in work_entry_point)
        }
        print('очистить не нужные точки входа:',filtered_result)
        return filtered_result

    except Exception as e:
        tb = traceback.format_exc()
        print(f"Ошибка произошла:\n{tb}")