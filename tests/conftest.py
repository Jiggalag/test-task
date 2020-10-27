import string

import pytest
import random
from api_helper import BearAPI


def generate_valid_bears(amount):
    result = list()
    for c in range(amount):
        result.append({
            "bear_type": random.choice(['POLAR', 'BROWN', 'BLACK', 'GUMMY']),
            "bear_name": ''.join(random.choice(string.ascii_uppercase) for _ in range(5)),
            "bear_age": random.uniform(0.0, 50.0)  # because bears cannot living more than 50 years
        })
    return result


def create_bears(api, amount):
    api.delete_all_bears()
    for bear in generate_valid_bears(amount):
        api.create_bear(bear)


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
    create_bears(api, 50)


@pytest.fixture(scope='function')
def single_bear(api):
    create_bears(api, 1)


@pytest.fixture(scope='function')
def two_bears(api):
    create_bears(api, 2)
