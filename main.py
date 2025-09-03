import os
import asyncio  # Импортируем asyncio для запуска асинхронной функции
from generator import generator
from generator_date.refPeriodEnd import refPeriodEnd
# from generator_date.refPeriodStart import refPeriodStart
from params_input import file_path
from parsing_taxonomy.dell_extra_entry_point import dell_extra_entry_point
from parsing_taxonomy.privod_k_standart_vid_spiska import privod_k_standart_vid_spiska
from parsing_taxonomy.read_taxonomy import read_taxonomy


# Этот скрипт предначзанчен для вычисления рабочих дат для НФО УК,УК_СПЕЦ_ДЕП,АИФ_УК
#Перед Запуском заполнить params_input.py!!!! версию таксономии, по выходным дням json
async def main():
    # 1 создать папку и файл настройка рабочих дат.conf
    mkdir_folder()

    # 2. читаем таксономию
    result = await read_taxonomy()
    result = await dell_extra_entry_point(result)
    auto_data_object = await privod_k_standart_vid_spiska(result)
    print('результат', auto_data_object)
    # 3. движок обработки
    generator(auto_data_object)


# 1. создать папку и файл настройка рабочих дат.conf
def mkdir_folder():
    # проверить если папка существует, если нет, то создать ее
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))


if __name__ == "__main__":
    asyncio.run(main())  # Запуск асинхронной функции
