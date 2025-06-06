import os

from generator import generator
from generator_date.refPeriodEnd import refPeriodEnd
# from generator_date.refPeriodStart import refPeriodStart
from params_input import file_path

# Этот скрипт предначзанчен для вычисления рабочих дат для НФО УК,УК_СПЕЦ_ДЕП,АИФ_УК
#Перед Запуском заполнить params_input!!!! версию таксономии, по выходным дням json
def main():
    # 1 cозадть папку и файл настройка рабочих дат.conf
    mkdir_folder()
    # 2 движок обработки
    generator()

# 1. # cозадть папку и файл настройка рабочих дат.conf
def mkdir_folder():
    # проверить если папка существует, если нет, то создать ее
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))

if __name__ == "__main__":
    main()