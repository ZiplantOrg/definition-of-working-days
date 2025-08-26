import os
import asyncio  # Импортируем asyncio для запуска асинхронной функции
from generator import generator
from generator_date.refPeriodEnd import refPeriodEnd
# from generator_date.refPeriodStart import refPeriodStart
from params_input import file_path
from parsing_taxonomy.read_taxonomy import read_taxonomy


# Этот скрипт предначзанчен для вычисления рабочих дат для НФО УК,УК_СПЕЦ_ДЕП,АИФ_УК
#Перед Запуском заполнить params_input.py!!!! версию таксономии, по выходным дням json
async def main():
    # 1 создать папку и файл настройка рабочих дат.conf
    mkdir_folder()

    # 2. читаем таксономию
    await read_taxonomy()
    # 3. движок обработки
    # generator()


# 1. создать папку и файл настройка рабочих дат.conf
def mkdir_folder():
    # проверить если папка существует, если нет, то создать ее
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))


if __name__ == "__main__":
    asyncio.run(main())  # Запуск асинхронной функции
