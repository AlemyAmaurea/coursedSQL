import pandas as pd
from sqlalchemy import create_engine
import psycopg2


class DataBaseManager:
    """Класс для передачи SQL запросов созданной базе данных"""
    pd.set_option('display.max_columns', None)

    def __init__(self, data_base_name: str, connection_settings):
        """
        При создании класса необходимо передать следующие аргументы:
        :param data_base_name: Наименование базы данных
        :param connection_settings: Настройки подключения к базе данных
        """
        self.__data_base_name = data_base_name
        self.__connection_settings = connection_settings

    def get_companies_and_vacancies_count(self) -> pd.DataFrame:
        """
        SQL запрос для получения списка всех компаний и количество вакансий у каждой компании.
        :return: Возвращает таблицу, согласно запросу
        """
        try:
            engine = create_engine(
                f'postgresql://{self.__connection_settings["user"]}:'
                f'{self.__connection_settings["password"]}@{self.__connection_settings["host"]}:'
                f'{self.__connection_settings["port"]}/{self.__data_base_name}')

            sql_query = """SELECT employer_title, vacancy_count
                            FROM public.employers"""
            result = pd.read_sql(sql_query, engine)
            return result

        except Exception as e:
            print('[ERROR] Ошибка при выполнении запроса')
            print(e)

        finally:
            engine.dispose()

    def get_all_vacancies(self) -> pd.DataFrame:
        """
        SQL запрос для получения списка список всех вакансий с указанием названия компании,
        названия вакансии и зарплаты и ссылки на вакансию.
        :return: Возвращает таблицу, согласно запросу
        """

        try:
            engine = create_engine(
                f'postgresql://{self.__connection_settings["user"]}:'
                f'{self.__connection_settings["password"]}@{self.__connection_settings["host"]}:'
                f'{self.__connection_settings["port"]}/{self.__data_base_name}')

            sql_query = """SELECT vacancy_title, employer_title, salary_from, salary_to, vacancies.url
                            FROM employers
                            JOIN public.vacancies USING(employer_id)"""

            result = pd.read_sql(sql_query, engine)
            return result

        except Exception as e:
            print('[ERROR] Ошибка при выполнении запроса')
            print(e)

        finally:
            engine.dispose()

    def get_avg_salary(self) -> pd.DataFrame:
        """
        SQL запрос для получения списка средних зарплат по вакансиям.
        :return: Возвращает таблицу, согласно запросу
        """

        try:
            engine = create_engine(
                f'postgresql://{self.__connection_settings["user"]}:'
                f'{self.__connection_settings["password"]}@{self.__connection_settings["host"]}:'
                f'{self.__connection_settings["port"]}/{self.__data_base_name}')

            sql_query = """SELECT vacancy_title, AVG((salary_from + salary_to) / 2) AS avg_salary, url
                            FROM public.vacancies
                            GROUP BY vacancy_title, url
                            ORDER BY avg_salary DESC"""

            result = pd.read_sql(sql_query, engine)
            return result

        except Exception as e:
            print('[ERROR] Ошибка при выполнении запроса')
            print(e)

        finally:
            engine.dispose()

    def get_vacancies_with_higher_salary(self) -> pd.DataFrame:
        """
        SQL запрос для получения списка всех вакансий, у которых зарплата выше средней по всем вакансиям.
        :return: Возвращает таблицу, согласно запросу
        """

        try:
            engine = create_engine(
                f'postgresql://{self.__connection_settings["user"]}:'
                f'{self.__connection_settings["password"]}@{self.__connection_settings["host"]}:'
                f'{self.__connection_settings["port"]}/{self.__data_base_name}')

            sql_query = """SELECT vacancy_title, salary_from, url
                            FROM vacancies
                            WHERE salary_from > (SELECT AVG((salary_from + salary_to) / 2) FROM vacancies)
                            ORDER BY salary_from DESC"""

            result = pd.read_sql(sql_query, engine)
            return result

        except Exception as e:
            print('[ERROR] Ошибка при выполнении запроса')
            print(e)

        finally:
            engine.dispose()

    def get_vacancies_with_keyword(self, keyword: str):
        """
        SQL запрос для получения списка всех вакансий, в названии которых содержатся переданные в метод слова.
        :return: Возвращает таблицу, согласно запросу
        """

        try:
            with psycopg2.connect(dbname=self.__data_base_name, **self.__connection_settings) as connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        f"""SELECT *
                        FROM vacancies
                        WHERE vacancy_title LIKE '%{keyword}%'""")

                    for i in cursor.fetchall()[:15]:
                        print(i)

        except Exception as e:
            print('[ERROR] Ошибка при выполнении запроса')
            print(e)

        finally:
            if connection:
                connection.close()