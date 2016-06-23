# encoding: utf-8

import datetime


def log(*args):
    print(datetime.datetime.now(), *args)


def test():
    log('test string', 42)


if __name__ == '__main__':
    test()