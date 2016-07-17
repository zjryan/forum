# encoding: utf-8

import datetime
import string
import hashlib


def log(*args):
    print(datetime.datetime.now(), *args)


def is_legal(s):
    for c in s:
        if c not in string.ascii_letters and \
        c not in string.digits:
            return False
    return True


def email_validate(email):
    if '@' not in email or '.' not in email:
        return False
    if email.find('@') > email.find('.'):
        return False
    # split email
    email_split = email.split('@')
    username = email_split[0] or None
    host_split = email_split[1].split('.')
    host = host_split[0] or None
    realm = host_split[1] or None

    if username is None or \
        host is None or \
        realm is None:
        return False
    return is_legal(username) and \
            is_legal(host) and \
            is_legal(realm)


encoding = 'utf-8'


def generate_password_hash(password):
    p = password.encode(encoding)
    return hashlib.sha1(p).hexdigest()


def check_password_hash(password_hash, password):
    hash = generate_password_hash(password)
    return password_hash == hash


def test_email_validate():
    test_item = [
        ('12345@qq.com', True),
        ('s2324hads@11', False),
        ('', False),
        ('sda.2231@qweq', False),
        ('@dsa.com', False),
        ('fsafaf.com', False),
    ]
    for t in test_item:
        email, expect = t
        actual = email_validate(email)
        assert actual == expect, \
            'assert error, email: {} || expect: {} || actual: {}'.format(email, expect, actual)


def test_password_hash():
    test_item = [
        (('dog', 'dog'), True),
        (('dog', 'cat'), False),
        (('', ''), True),
        (('safdfadgavczfgdzgsrtrgsfgvb', 'afdavbf'), False),
        (('faferb', ''), False),
    ]
    for t in test_item:
        password, expect = t
        password_hash = generate_password_hash(password[0])
        actual = check_password_hash(password_hash, password[1])
        assert actual == expect, \
            'assert error, password: {} || expect: {} || actual: {}'.format(password, expect, actual)


if __name__ == '__main__':
    test_password_hash()
    test_email_validate()