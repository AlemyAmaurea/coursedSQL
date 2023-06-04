import requests
import csv


class VacanciesParser:
    """Класс для парсинга вакансий работодателя"""

    __vacancy_url = 'https://api.hh.ru/vacancies'

    def __init__(self):
        self.__vacancies_list = []
        self.__pages_for_parse = 5

    def __parsing_process(self, indexes, pages) -> list[dict]:
        """
        Скрытый метод для получения информации со всех страниц
        :param indexes: id компаний работодателя, полученные методом 'get_employers_id'
        :param pages: Вспомогательная переменная
        :return: Списковый словарь, содержащий информацию о всех вакансиях выбранных компаний
        """

        params = {'employer_id': indexes,
                  'page': self.__pages_for_parse,
                  'per_page': 100}
        return requests.get(self.__vacancy_url, params=params).json()['items']

    def get_employers_vacancies(self, indexes: list) -> list:
        """
        Метод позволяет получить информацию о вакансиях компаний
        :param indexes: id компаний работодателя, полученные методом 'get_employers_id'
        :return: Списковый словарь, содержащий информацию о всех вакансиях выбранных компаний
        """

        for employer_id in indexes:
            for page in range(0, self.__pages_for_parse):
                params = {'employer_id': employer_id,
                          'page': page,
                          'per_page': 100}
                response = requests.get(self.__vacancy_url, params=params)
                if response.ok:
                    data = response.json()['items']
                    if len(data) == 0:
                        break
                    self.__vacancies_list.extend(data)
                else:
                    break

        return self.__vacancies_list

    def save_data_as_csv(self, filename: str, data: list[dict]) -> None:
        """
        Метод для сохранения итоговой информации о компаниях в формате csv
        :param filename: Необходимо передать названия файла, для сохранения информации
        :param data: Списковый словарь с информацией о вакансиях, полученной в результате парсинга
        """

        filename = f"{filename.capitalize().strip()}_vacancies.csv"

        with open(filename, mode='w', newline='', encoding='utf-8') as csv_file:

            fieldnames = ['employer_id', 'vacancy_title',
                          'salary_from', 'salary_to', 'url']
            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            for item in data:

                if item['salary'] is None:
                    salary_from = 0
                    salary_to = 0

                else:
                    salary_from = 0 if not item['salary']['from'] else item['salary']['from']
                    salary_to = 0 if not item['salary']['to'] else item['salary']['to']

                writer.writerow(
                    {'employer_id': int(item['employer'].get('id')),
                     'vacancy_title': str(item.get('name')),
                     'salary_from': f"{float(salary_from)}",
                     'salary_to': f"{float(salary_to)}",
                     'url': str(item.get('alternate_url'))})