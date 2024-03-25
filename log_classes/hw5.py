from urllib.request import urlopen
from collections import Counter
from datetime import datetime, date
import unittest
import re

TEST_LOG = 'http://shannon.usu.edu.ru/ftp/python/hw4/test.log'


def make_stat():
    stat = LogStatParser()
    return stat


class LogStatParser:
    def __init__(self) -> None:
        self._log = []
        self._regex = re.compile(r'^(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}) - - ' +
                                 r'\[(\d{2}/[\w]+?/\d{4})[\w\s:+]*?\] ' +
                                 r'["\'][A-Za-z]+? (.*?) HTTP.*?["\'] ' +
                                 r'[\d\s]*? ["\'].*?["\'] ["\'](.*?)["\'] ' +
                                 r'([\d]+)$', re.IGNORECASE)

    def add_line(self, line: str) -> None:
        request = self._regex.search(line)
        if not request:
            return None

        client, day, page, browser, response_time = request.groups()
        self._log.append({
            'client': client,
            'day': day,
            'page': page,
            'browser': browser,
            'response_time': response_time
        })

    def results(self) -> dict:
        stat = {
            'FastestPage': self.fastest_page,
            'MostActiveClient': self.most_active_client,
            'MostActiveClientByDay': self.most_active_client_by_day,
            'MostPopularBrowser': self.most_popular_browser,
            'MostPopularPage': self.most_popular_page,
            'SlowestAveragePage': self.slowest_average_page,
            'SlowestPage': self.slowest_page
        }
        return stat

    @property
    def fastest_page(self) -> str:
        if not self._log:
            return None
        requests = [(request['page'], request['response_time'])
                    for request in self._log]
        page = min(requests, key=lambda x: int(x[1]))[0]
        return page

    @property
    def slowest_page(self) -> str:
        if not self._log:
            return None
        requests = [(request['page'], request['response_time'])
                    for request in self._log]
        page = max(requests, key=lambda x: int(x[1]))[0]
        return page

    @property
    def slowest_average_page(self) -> str:
        if not self._log:
            return None
        requests = [(request['page'], request['response_time'])
                    for request in self._log]
        pages_response_time = {}
        for page, response_time in requests:
            if page not in pages_response_time:
                pages_response_time[page] = [response_time]
            else:
                pages_response_time[page].append(response_time)
        for page, response_time in pages_response_time.items():
            response_time = list(map(int, response_time))
            pages_response_time[page] = sum(response_time) / len(response_time)
        page = max(pages_response_time, key=pages_response_time.get)
        return page

    @property
    def most_active_client(self) -> str:
        if not self._log:
            return None
        clients = [request['client'] for request in self._log]
        client = Counter(clients).most_common(1)[0][0]
        return client

    @property
    def most_active_client_by_day(self) -> dict:
        if not self._log:
            return None
        request_days = {}
        for request in self._log:
            client = request['client']
            day = request['day']
            if client not in request_days:
                request_days[client] = [day]
            else:
                request_days[client].append(day)
        for client, days in request_days.items():
            request_days[client] = Counter(days).most_common(1)[0]
        client = max(request_days, key=lambda x: x[1])
        client_date = datetime.strptime(
            request_days[client][0], '%d/%b/%Y').date()
        return {client_date: client}

    @property
    def most_popular_browser(self) -> str:
        if not self._log:
            return None
        browsers = [request['browser'] for request in self._log]
        browser = Counter(browsers).most_common(1)[0][0]
        return browser

    @property
    def most_popular_page(self) -> str:
        if not self._log:
            return None
        pages = [request['page'] for request in self._log]
        page = Counter(pages).most_common(1)[0][0]
        return page


class LogStatTests(unittest.TestCase):
    def setUp(self):
        with urlopen(TEST_LOG) as f:
            self.data = f.read().decode('utf-8').split('\n')

        self.stat = make_stat()
        for line in filter(lambda s: 'OPTION' not in s, self.data):
            self.stat.add_line(line)

    def test_fastest_page(self):
        self.assertEqual(self.stat.fastest_page, '/img/r.png')

    def test_most_active_client(self):
        self.assertEqual(self.stat.most_active_client, '192.168.12.155')

    def test_most_active_client_by_day(self):
        self.assertEqual(self.stat.most_active_client_by_day,
                         {date(2012, 7, 8): '192.168.12.155'})

    def test_most_popular_browser(self):
        self.assertEqual(self.stat.most_popular_browser,
                         'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.1; '
                         'Trident/4.0; SLCC2; .NET CLR 2.0.50727; .NET CLR '
                         '3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; '
                         'Tablet PC 2.0; .NET4.0C; .NET4.0E; InfoPath.3; '
                         'MS-RTC LM 8)')

    def test_most_popular_page(self):
        self.assertEqual(self.stat.most_popular_page, '/menu-top.php')

    def test_slowest_average_page(self):
        self.assertEqual(self.stat.slowest_average_page, '/call_centr.php')

    def test_slowest_page(self):
        self.assertEqual(self.stat.slowest_page, '/menu-top.php')


if __name__ == '__main__':
    unittest.main()
