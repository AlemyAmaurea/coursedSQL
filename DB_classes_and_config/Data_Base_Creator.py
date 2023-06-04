import csv
import psycopg2


class DataBaseCreator:
    """Класс для создания базы данных и ее наполнения данными"""

    def __init__(self, data_base_name: str, connection_settings):
        """
        :param data_base_name: Наименование базы данных в строковом виде
        :param connection_settings: Параметры соединения с базой данных
        """
        self.__data_base_name = data_base_name
        self.__connection_settings = connection_settings

    def create_data_base(self):
        """Метод для создания базы данных"""

        try:
            connection = psycopg2.connect(dbname='postgres', **self.__connection_settings)
            connection.set_session(autocommit=True)
            cursor = connection.cursor()
            cursor.execute(f"DROP DATABASE IF EXISTS {self.__data_base_name}")
            cursor.execute(f"CREATE DATABASE {self.__data_base_name}")
            print(f"[INFO] База данных {self.__data_base_name} успешно создана")

            cursor.close()
            connection.close()

        except Exception as e:
            print("[ERROR] Не удалось создать базу данных")
            print(e)

    def create_tables(self) -> None:
        """Метод для создания двух таблиц: employers и vacancies"""

        try:
            with psycopg2.connect(dbname=self.__data_base_name, **self.__connection_settings) as connection:
                with connection.cursor() as cursor:
                    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS public.employers (
                        employer_id int PRIMARY KEY,
                        employer_title varchar(100) NOT NULL,
                        vacancy_count int,
                        url varchar(255) NOT NULL)
                    """)

                    print("[INFO] Таблица employers успешно создана")

                with connection.cursor() as cursor:
                    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS public.vacancies (
                        employer_id int,
                        vacancy_title varchar(100) NOT NULL,
                        salary_from real,
                        salary_to real,
                        url varchar(255) NOT NULL,
                        FOREIGN KEY (employer_id) REFERENCES public.employers(employer_id)) 
                    """)

                    print("[INFO] Таблица vacancies успешно создана")

        except Exception as e:
            print("[ERROR] Не удалось создать таблицу")
            print(e)

        finally:
            if connection:
                connection.close()

    def fill_the_tables(self, employers_data, vacancies_data) -> None:
        """
        Метод для наполнения таблиц данными, полученными в результате парсинга HH
        :param employers_data: Файл в формате csv, содержащий информацию о работодателях
        :param vacancies_data: Файл в формате csv, содержащий информацию о вакансиях
        """
        try:
            with psycopg2.connect(dbname=self.__data_base_name, **self.__connection_settings) as connection:
                with connection.cursor() as cursor:

                    with open(employers_data) as file:
                        file_reader = csv.DictReader(file, delimiter=',')

                        for i in file_reader:
                            employer_id = i.get('employer_id')
                            employer_title = i.get('employer_title')
                            vacancy_count = i.get('vacancy_count')
                            url = i.get('url')

                            cursor.executemany(
                                'INSERT INTO public.employers VALUES (%s, %s, %s, %s)',
                                [(employer_id, employer_title, vacancy_count, url)])

                        print('[INFO] Таблица employers успешно заполнена данными')

                    with open(vacancies_data, encoding='utf-8') as file:
                        file_reader = csv.DictReader(file, delimiter=',')

                        for i in file_reader:
                            employer_id = i.get('employer_id')
                            vacancy_title = i.get('vacancy_title')
                            salary_from = i.get('salary_from')
                            salary_to = i.get('salary_to')
                            url = i.get('url')

                            cursor.executemany(
                                'INSERT INTO public.vacancies VALUES (%s, %s, %s, %s, %s)',
                                [(employer_id, vacancy_title, salary_from, salary_to, url)])

                        print('[INFO] Таблица vacancies успешно заполнена данными')

        except Exception as e:
            print('[ERROR] Не удалось заполнить таблицы')
            print(e)

        finally:
            if connection:
                connection.close()