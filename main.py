import os

from generator import generator
from generator_date.refPeriodEnd import refPeriodEnd
from generator_date.refPeriodStart import refPeriodStart
from params_input import file_path


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

    # # создать файл
    # with open(os.path.join(file_path, 'настройка рабочих дат.conf'), 'w') as file:
    #     file.write("")


if __name__ == "__main__":
    main()