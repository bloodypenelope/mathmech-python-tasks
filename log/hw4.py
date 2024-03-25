from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from collections import Counter
from itertools import chain
import argparse
import sys
import re


TEST_LOG = 'https://shannon.usu.edu.ru/ftp/python/hw4/test.log'

regex = re.compile(r'^(\d{1,3}.\d{1,3}.\d{1,3}.\d{1,3}) - - \[(\d{2}/[\w]+?/\d{4})[\w\s:+]*?\] "GET (.*?) HTTP/1.1" [\d\s]*? ".*?" "(.*?)" ([\d]+)\n$')


def read_log(log):
    users = {}
    try:
        with urlopen(log) as f:
            for line in f:
                if regex.search(line.decode()):
                    print(regex.search(line.decode())[0])

                line = line.split()

                if b'"GET' not in line:
                    continue
                request_index = line.index(b'"GET')

                user = line[0].decode()
                page = line[request_index + 1].decode()

                if user not in users:
                    users[user] = [page]
                else:
                    users[user].append(page)
        return users
    except (URLError, HTTPError, ValueError):
        return None


def most_active_client(users):
    client = max(users, key=lambda x: len(users[x]))
    return client


def most_popular_page(users):
    count = Counter(users.keys())
    count.update(chain.from_iterable(users.values()))
    page = count.most_common(1)[0][0]
    return page


def parse_args():
    parser = argparse.ArgumentParser(description='Log parser')
    parser.add_argument('filename', action='store', nargs=1,
                        help='URL of a log file to parse')
    parser.add_argument('-u', '--user', action='store_true', required=False,
                        default=False, help='displays the most active user')
    parser.add_argument('-p', '--page', action='store_true', required=False,
                        default=False, help='displays the most popular page')
    return parser.parse_args()


def main():
    args = parse_args()
    users = read_log(args.filename[0])
    if not users:
        print('Invalid file URL')
        sys.exit(1)
    if not args.user and not args.page:
        print('No additional arguments were provided (-h for help)')
        sys.exit(2)
    if args.user:
        print(f'Most active user: {most_active_client(users)}')
    if args.page:
        print(f'Most popular page: {most_popular_page(users)}')
    sys.exit(0)


if __name__ == '__main__':
    main()
