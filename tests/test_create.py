import random
import string

import pytest
# import sys, os
# myPath = os.path.dirname(os.path.abspath(__file__))
# sys.path.insert(0, myPath + '/../')
# print(sys.path)

url = '0.0.0.0'
port = '8091'


positive_types = [
        'POLAR',
        'BROWN',
        'BLACK',
        'GUMMY'
    ]

success_type = [
    'POLAR'
]

negative_types = [
        'INCORRECT',
        None,
        '',
        ' ' * 200,
        True,
        123,
        ' ' * 500 + ';\n\n\n\n\n DROP TABLE bears;'
    ]

positive_names = [
        'mikhail',
        'Bear',
        'MISHA',
        'ПЕТЯ',
        'Михайло Потапыч Медведев',
        '123',
        '!@#'
    ]

success_name = ['BEAR']

negative_names = [
        None,
        123,
        '',
        ' ' * 200,
        True,
        ' ' * 500 + ';\n\n\n\n\n DROP TABLE bears;'
    ]


positive_ages = [
        0.0,
        0.2,
        1.0,
        10.0
    ]

success_age = [
    10.0
]

negative_ages = [
       - 1000000,
       - 1.0,
       - 0.1,
       100,
       None,
       '123'
    ]


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


def is_not_single(bears):
    if len(bears) != 1:
        return f"Incorrect lenght of response! Expected 1, got {len(bears)}"
    else:
        return ''


def is_invalid(request_bear, result):
    result.pop('bear_id')
    errors = list()
    if result != request_bear:
        for item in ['bear_type', 'bear_name', 'bear_age']:
            if result.get(item) != request_bear.get(item):
                errors.append(f'Incorrect {item}! Expected: {request_bear.get(item)}, got: {result.get(item)}')
            result.pop(item)
            request_bear.pop(item)
        if result:
            errors.append(f'There is excess keys founded in result: {result.keys()}')
    return errors


@pytest.mark.parametrize("bear_type", positive_types)
@pytest.mark.parametrize("name", positive_names)
@pytest.mark.parametrize("age", positive_ages)
@pytest.mark.usefixtures('no_bears')
def test_positive_create_single_bear(api, bear_type, name, age):
    insert_bear = {'bear_type': bear_type, 'bear_name': name, 'bear_age': age}
    api.create_bear(insert_bear)
    bears = api.get_all_bears()
    errors = is_invalid(insert_bear, bears[0])
    assert not any([is_not_single(bears), errors]), 'errors occured:\n{}'.format('\n'.join(errors))


@pytest.mark.parametrize("bear_type", negative_types)
@pytest.mark.parametrize("name", negative_names)
@pytest.mark.parametrize("age", negative_ages)
@pytest.mark.usefixtures('no_bears')
@pytest.mark.xfail
def test_negative_create_single_bear(api, bear_type, name, age):
    insert_bear = {'bear_type': bear_type, 'bear_name': name, 'bear_age': age}
    api.create_bear(insert_bear)
    bears = api.get_all_bears()
    errors = is_invalid(insert_bear, bears[0])
    assert any([is_not_single(bears), errors]), 'errors occured:\n{}'.format('\n'.join(errors))


@pytest.mark.usefixtures('no_bears')
def test_create_identical_bears(api):
    bear = generate_valid_bears(1)[0]
    api.create_bear(bear)
    api.create_bear(bear)
    bears = api.get_all_bears()
    errors = list()
    id1 = bears[0].pop('bear_id')
    id2 = bears[1].pop('bear_id')
    if id1 == id2:
        errors.append(f'Id for identical entities are same! bear_id: {id1}')
    if bears[0] != bears[1]:
        if bears[0].keys() != bears[1].keys():
            errors.append(f'Different keys! bear0: {bears[0].keys()}, bear1: {bears[1].keys()}')
        else:
            for key in bears[0].keys():
                if bears[0].get(key) != bears[1].get(key):
                    errors.append(f'Values for key {key} differs! bear0: {bears.get(key)}, bear1: {bears.get(key)}')
    assert errors, 'errors occured:\n{}'.format('\n'.join(errors))


@pytest.mark.usefixtures('no_bears')
def test_less_params(api):
    for key in ['bear_type', 'bear_name', 'bear_age']:
        bear = generate_valid_bears(1)[0]
        bear.pop(key)
        api.create_bear(bear)
        bears = api.get_all_bears()
        assert not bears, f'Bear created incorrectly without important parameter {key}'


# Probably we should ignore unknown fields in request json and if json have all neccessary fields - system should
# creates bear. If not - this test invalid
@pytest.mark.usefixtures('no_bears')
def test_more_params(api):
    bear = generate_valid_bears(1)[0]
    bear.update({"excess_parameter": "test"})
    api.create_bear(bear)
    bears = api.get_all_bears()
    bear.pop("excess_parameter")
    errors = is_invalid(bear, bears[0])
    assert not any([is_not_single(bears), errors]), 'errors occured:\n{}'.format('\n'.join(errors))


if __name__ == '__main__':
    pytest.main(['-qq'])
