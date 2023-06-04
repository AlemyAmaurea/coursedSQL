import requests
import csv


class EmployersParser:
    """Класс для парсинга компаний работодателя"""

    __employer_url = 'https://api.hh.ru/employers?only_with_vacancies=true'

    def get_employers_data(self, key_word: str) -> list[dict]:
        """
        Метод позволяет получить информацию о 10 компаниях
        :param key_word: Ключевое слово, которое будет использоваться для поиска в наименовании компании или ее описании
        :return: Список словарей, содержащих полную информацию о компании работодателя
        """
        params = {'text': key_word.lower(),
                  'per_page': 10,
                  'area': '113'}
        response = requests.get(self.__employer_url, params=params).json()['items']
        return response

    def get_employers_id(self, data: list[dict]) -> list:
        """
        Метод позволяет получить id компаний работодателя для дальнейшего поиска их вакансий
        :param data: Для получения id необходимо передать список,
        полученный ранее списковый словарь с информацией о компаниях
        :return: Список, содержащий id компаний работодателя
        """

        id_list = []
        for i in data:
            id_list.append(i.get('id'))

        return id_list

    def save_as_csv(self, filename: str, data: list[dict]) -> None:
        """
        Метод для сохранения итоговой информации о компаниях в формате csv
        :param filename: Необходимо передать названия файла, для сохранения информации
        :param data: Списковый словарь с информацией о компаниях, полученной в результате парсинга
        """
        filename = f"{filename.capitalize().strip()}_employers.csv"

        with open(filename, mode='w', newline='') as csv_file:
            fieldnames = ['employer_id', 'employer_title', 'vacancy_count', 'url']

            writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

            writer.writeheader()
            for item in data:
                writer.writerow(
                    {'employer_id': int(item.get('id')),
                     'employer_title': str(item.get('name')),
                     'vacancy_count': int(item.get('open_vacancies')),
                     'url': str(item.get('alternate_url'))})