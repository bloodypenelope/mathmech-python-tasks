from urllib.request import urlopen
from datetime import datetime, timezone
import unittest
import re

TEST_LOG = 'http://shannon.usu.edu.ru/ftp/python/hw4/test.log'


def merge(*iterables, key=None):
    """Функция склеивает упорядоченные по ключу `key` и порядку «меньше»
    коллекции из `iterables`.

    Результат — итератор на упорядоченные данные.
    В случае равенства данных следует их упорядочить в порядке следования
    коллекций"""
    merged_iterables = []
    for iterable in iterables:
        merged_iterables.extend(iterable)
    sorted_iterables = sorted(merged_iterables, key=key)
    return iter(sorted_iterables)


def log_key(s: str) -> float:
    """Функция по строке лога возвращает ключ для её сравнения по времени"""
    regex = re.compile(r'(\[\d{2}/[\w]+?/\d{4}[\w\s:+]*?\])')
    match = regex.search(s)
    if not match:
        return 0.0
    day = datetime.strptime(match[1], '[%d/%b/%Y:%H:%M:%S %z]')
    epoch = datetime.fromtimestamp(0, tz=timezone.utc)
    return (day - epoch).total_seconds()


class TestTest(unittest.TestCase):
    def setUp(self):
        with urlopen(TEST_LOG) as f:
            self.data = f.read().decode('utf-8').split('\n')

    def test_is_iterator(self):
        test = merge()
        self.assertTrue(hasattr(test, '__iter__')
                        and hasattr(test, '__next__'))

    def test_no_args(self):
        test = merge()
        self.assertEqual(list(test), [])

    def test_key_func(self):
        iterable = [('A', 1), ('B', 3), ('C', 2)]
        test = merge(iterable, key=lambda x: x[1])
        self.assertEqual(list(test), [('A', 1), ('C', 2), ('B', 3)])

    def test_one_sequence(self):
        iterable = (1, 6, 2, 8)
        test = merge(iterable)
        self.assertEqual(list(test), [1, 2, 6, 8])

    def test_two_sequences_eq_size(self):
        iterables = [(1, 2, 8), (4, 3, 5)]
        test = merge(*iterables)
        self.assertEqual(list(test), [1, 2, 3, 4, 5, 8])

    def test_two_sequences_neq_size(self):
        iterables = [(1, 7), (2, 5, 6)]
        test = merge(*iterables)
        self.assertEqual(list(test), [1, 2, 5, 6, 7])

    def test_log_merge(self):
        test_log = self.data[:100]
        test = merge(test_log, key=log_key)
        test = map(lambda x: int(x.split()[-1]), test)
        expected_data = [1423, 67, 71, 366, 64]
        self.assertEqual(list(test)[:5], expected_data)


if __name__ == '__main__':
    unittest.main()
