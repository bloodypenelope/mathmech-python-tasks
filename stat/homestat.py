import re


def make_stat(filename: str) -> dict:
    """
    Функция вычисляет статистику по именам за каждый год с учётом пола.
    """
    stat = {}
    with open(filename, encoding='cp1251') as f:
        regex_year = re.compile(r'(?<=<h3>)([0-9]*?)(?=</h3>)')
        regex_name = re.compile(r'(?<=\s)([А-ЯЁа-яё]*?)(?=</a>)')
        regex_exc = re.compile(r'^Илья|Никита|Игорь|Лёва$')
        regex_female = re.compile(r'[аяь]$')
        for line in f:
            match_year = regex_year.search(line)
            match_name = regex_name.search(line)
            if match_year:
                year = match_year[0]
            if match_name:
                name = match_name[0]
                sex = 'male'
                match_female = regex_female.search(name)
                match_exc = regex_exc.search(name)
                if match_female and not match_exc:
                    sex = 'female'
                if name not in stat:
                    stat[name] = [sex, year]
                else:
                    stat[name].append(year)
    return stat


def extract_years(stat: dict) -> list:
    """
    Функция принимает на вход вычисленную статистику и выдаёт список годов,
    упорядоченный по возрастанию.
    """
    years = [year for value in stat.values() for year in value[1:]]
    years = sorted(set(years))
    return years


def extract_general(stat: dict) -> list:
    """
    Функция принимает на вход вычисленную статистику и выдаёт список tuple'ов
    (имя, количество) общей статистики для всех имён.
    Список должен быть отсортирован по убыванию количества.
    """
    general = [(name, len(item) - 1) for name, item in stat.items()]
    general = sorted(general, key=lambda x: x[1], reverse=True)
    return general


def extract_general_male(stat: dict) -> list:
    """
    Функция принимает на вход вычисленную статистику и выдаёт список tuple'ов
    (имя, количество) общей статистики для имён мальчиков.
    Список должен быть отсортирован по убыванию количества.
    """
    general_male = [(name, len(item) - 1) for name, item in stat.items()
                    if item[0] == 'male']
    general_male = sorted(general_male, key=lambda x: x[1], reverse=True)
    return general_male


def extract_general_female(stat: dict) -> list:
    """
    Функция принимает на вход вычисленную статистику и выдаёт список tuple'ов
    (имя, количество) общей статистики для имён девочек.
    Список должен быть отсортирован по убыванию количества.
    """
    general_female = [(name, len(item) - 1) for name, item in stat.items()
                      if item[0] == 'female']
    general_female = sorted(general_female, key=lambda x: x[1], reverse=True)
    return general_female


def extract_year(stat: dict, year: str) -> list:
    """
    Функция принимает на вход вычисленную статистику и год.
    Результат — список tuple'ов (имя, количество) общей статистики для всех
    имён в указанном году.
    Список должен быть отсортирован по убыванию количества.
    """
    year_list = [(name, item.count(year)) for name, item in stat.items()
                 if year in item]
    year_list = sorted(year_list, key=lambda x: x[1], reverse=True)
    return year_list


def extract_year_male(stat: dict, year: str) -> list:
    """
    Функция принимает на вход вычисленную статистику и год.
    Результат — список tuple'ов (имя, количество) общей статистики для всех
    имён мальчиков в указанном году.
    Список должен быть отсортирован по убыванию количества.
    """
    year_male = [(name, item.count(year)) for name, item in stat.items()
                 if year in item and item[0] == 'male']
    year_male = sorted(year_male, key=lambda x: x[1], reverse=True)
    return year_male


def extract_year_female(stat: dict, year: str) -> list:
    """
    Функция принимает на вход вычисленную статистику и год.
    Результат — список tuple'ов (имя, количество) общей статистики для всех
    имён девочек в указанном году.
    Список должен быть отсортирован по убыванию количества.
    """
    year_male = [(name, item.count(year)) for name, item in stat.items()
                 if year in item and item[0] == 'female']
    year_male = sorted(year_male, key=lambda x: x[1], reverse=True)
    return year_male


if __name__ == '__main__':
    pass
