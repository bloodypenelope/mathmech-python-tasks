#!/usr/bin/env python3
import re
import sys
import time
from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from urllib.parse import quote, unquote


def get_content(name):
    """
    Функция возвращает содержимое вики-страницы name из русской Википедии.
    В случае ошибки загрузки или отсутствия страницы возвращается None.
    """
    try:
        with urlopen('https://ru.wikipedia.org/wiki/' + quote(name)) as page:
            return page.read().decode('utf-8', errors='ignore')
    except (URLError, HTTPError):
        return None


def extract_content(page):
    """
    Функция принимает на вход содержимое страницы и возвращает 2-элементный
    tuple, первый элемент которого — номер позиции, с которой начинается
    содержимое статьи, второй элемент — номер позиции, на котором заканчивается
    содержимое статьи.
    Если содержимое отсутствует, возвращается (0, 0).
    """
    start = page.find(r'<div class="mw-content-ltr mw-parser-output"')
    if start == -1:
        return 0, 0
    end = page.find(r'<!--esi')
    return start, end


def extract_links(page, begin, end):
    """
    Функция принимает на вход содержимое страницы и начало и конец интервала,
    задающего позицию содержимого статьи на странице и возвращает все имеющиеся
    ссылки на другие вики-страницы без повторений и с учётом регистра.
    """
    regex = re.compile(r'<a\s+href=["\']/wiki/([\w%]*?)["\']', re.IGNORECASE)
    page = page[begin:end]
    links = regex.findall(page)
    links = set(map(unquote, links))
    return links


def find_chain(start, finish):
    """
    Функция принимает на вход название начальной и конечной статьи и возвращает
    список переходов, позволяющий добраться из начальной статьи в конечную.
    Первым элементом результата должен быть start, последним — finish.
    Если построить переходы невозможно, возвращается None.
    """
    if start == finish:
        return [start]

    queue = [[start]]
    visited = set()

    while queue:
        path = queue.pop(0)
        node = path[-1]
        print(node)

        if node in visited:
            continue
        visited.add(node)

        page = get_content(node)
        if not page:
            continue

        content = extract_content(page)
        if content == (0, 0):
            continue

        links = extract_links(page, content[0], content[1])

        for link in links:
            new_path = list(path)
            new_path.append(link)

            if link == finish:
                return new_path

            queue.append(new_path)


def main():
    print(quote('Настоящее'))
    if len(sys.argv) == 2:
        start = sys.argv[1]
        finish = "Философия"
        path = find_chain(start, finish)
        if path:
            print(path)


if __name__ == '__main__':
    start_time = time.time()
    main()
    print(f'--- {time.time() - start_time} seconds ---')
