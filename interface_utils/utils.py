import time
from DB_classes_and_config.Data_Base_Creator import DataBaseCreator
from DB_classes_and_config.Data_Base_Manager import DataBaseManager
from DB_classes_and_config.config import config
from Employers_parser.Employers_Parser import EmployersParser
from Vacancies_parser.Vacancies_Parser import VacanciesParser


def user_interface():
    while True:

        company_keyword = input(
            'Введите ключевое слово, которое содержится в названии компании или его описании: ').lower().strip()

        while company_keyword == '':
            company_keyword = input('Наименование не может быть пустым, повторите ввод: ').strip()

        ep = EmployersParser()
        employers_data = ep.get_employers_data(company_keyword)

        print('\nИдет процесс парсинга информации о работодателях и их вакансиях.\n'
              'По завершении вы получите 2 csv файла, содержащие информацию о работодателях и их вакансиях...')

        ep.save_as_csv(company_keyword, employers_data)
        emp_indexes = ep.get_employers_id(employers_data)

        vp = VacanciesParser()
        vacancies_data = vp.get_employers_vacancies(emp_indexes)
        vp.save_data_as_csv(company_keyword, vacancies_data)
        print(f"[INFO] Файл {company_keyword.capitalize()}_employers.csv успешно создан")
        print(f"[INFO] Файл {company_keyword.capitalize()}_vacancies.csv успешно создан")

        db_name = input(
            '\nВведите наименование базы данных, для ее создания '
            'и дальнейшего с ней взаимодействия: ').lower().replace(' ', '').strip()

        while db_name.replace(' ', '') == '' or db_name.isdigit():
            db_name = input(
                'Наименование базы данных должно быть строкового типа и состоять из букв!\n'
                'Пожалуйста, повторите ввод: ').lower().replace(' ', '').strip()

        print(f"Идет процесс создания базы данных {db_name}...")
        print(f"Идет процесс создания таблиц 'employers' и 'vacancies'...\n")

        time.sleep(2)

        params = config()
        dbc = DataBaseCreator(db_name, params)
        dbc.create_data_base()
        dbc.create_tables()
        dbc.fill_the_tables(f"{company_keyword.capitalize()}_employers.csv",
                            f"{company_keyword.capitalize()}_vacancies.csv")

        dbm = DataBaseManager(db_name, config())

        available_commands = "\nТеперь вам доступны следующие запросы для взаимодействия с базой данных:\n" \
                             "1. Список всех компаний и количество вакансий у каждой компании.\n" \
                             "2. Список всех вакансий с указанием названия компании, названия вакансии, " \
                             "зарплаты и ссылки на вакансию.\n" \
                             "3. Информация о средней зарплате по вакансиям.\n" \
                             "4. Список вакансий, у которых зарплата выше средней относительно всех вакансий.\n" \
                             "5. Поиск вакансий, содержащих ключевое слово в наименовании.\n" \
                             "6. Завершение работы программы.\n" \
                             "*Помощь. Повторный вывод всех доступных к использованию команд.\n"
        print(available_commands)

        user_command = input('Для выбора команды, введите ее номер: ').lower().strip()
        print()

        while user_command != '6':

            if user_command == 'помощь':
                print(available_commands)

            if user_command == '1':
                print('Список всех компаний и количество вакансий у каждой компании.')
                print(dbm.get_companies_and_vacancies_count())

            if user_command == '2':
                print('Список всех вакансий с указанием названия компании, названия вакансии, '
                      'зарплаты и ссылки на вакансию')
                print(dbm.get_all_vacancies())

            if user_command == '3':
                print('Информация о средней зарплате по вакансиям')
                print(dbm.get_avg_salary())

            if user_command == '4':
                print('Список вакансий, у которых зарплата выше средней относительно всех вакансий')
                print(dbm.get_vacancies_with_higher_salary())

            if user_command == '5':
                print('Поиск вакансий, содержащих ключевое слово в наименовании.'
                      '[INFO] Регистр первой буквы в ключевом слове имеет значение!')
                vacancy_keyword = input('Введите ключевое слово для поиска вакансии: ').strip()

                while not vacancy_keyword.replace(' ', '').strip().isalpha():
                    vacancy_keyword = input('Ключевое слово должно быть строкового типа\n'
                                            'Пожалуйста, повторите ввод: ').strip()

                dbm.get_vacancies_with_keyword(vacancy_keyword)

            elif user_command not in ('1', '2', '3', '4', '5', 'помощь'):
                print('Команда не найдена, пожалуйста, повторите ввод')

            user_command = input('\nДля выбора команды, введите ее номер: ').lower().strip()
            print()

        print('Действие программы завершено!')
        exit(0)