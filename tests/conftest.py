import string

import pytest
import random
from api_helper import BearAPI


def generate_valid_bears(amount):
    result = list()
    for c in range(amount):
        result.append({"bear_type": get_type(), "bear_name": get_name(), "bear_age": get_age()})
    return result


def get_type():
    return random.choice(['POLAR', 'BROWN', 'BLACK', 'GUMMY'])


def get_age():
    return random.uniform(0.0, 50.0)  # because bears cannot living


def get_name():
    return ''.join(random.choice(string.ascii_uppercase) for _ in range(5))


@pytest.fixture(scope='session')
def api():
    url = '0.0.0.0'
    port = '8091'
    return BearAPI(url, port)


@pytest.fixture(scope='function')
def no_bears(api):
    api.delete_all_bears()
    if api.get_all_bears():
        print('Seems like delete_all_bears method is not worked')
        raise ValueError


@pytest.fixture(scope='function')
def many_bears(api):
    api.delete_all_bears()
    for bear in generate_valid_bears(50):
        api.create_bear(bear)


@pytest.fixture(scope='function')
def single_bear(api):
    api.delete_all_bears()
    api.create_bear({"bear_type": "POLAR", "bear_name": "BEAR", "bear_age": 7.0})
