import math
import pytest
import random
import string


url = '0.0.0.0'
port = '8091'


positive_types = [
        'POLAR',
        'BROWN',
        'BLACK',
        'GUMMY'
    ]

negative_types = [
        'INCORRECT',
        None,
        '',
        ' ' * 200,
        True,
        123,
        '[POLAR]',
        '{POLAR}',
        ' ' * 500 + ';\n\n\n\n\n DROP TABLE bears;'
    ]

positive_names = [
        'mikhail',
        'Bear',
        'MISHA',
        '   BEAR',
        'Michael O`Bear',
        'sir Bear-de-Grizly',
        'BEAR   ',
        '   BEAR   ',
        'ПЕТЯ',
        'Михайло Потапыч Медведев',
        "".join(random.choice(string.ascii_lowercase) for i in range(100)),
        '123',
        '!@#$%^&*():"{}/\|'
    ]

negative_names = [
        None,
        123,
        '',
        ' ' * 200,
        True,
        {"2": "3"},
        dict(),
        list(),
        '[NAME]',
        '{NAME}',
        ' ' * 500 + ';\n\n\n\n\n DROP TABLE bears;'
    ]


positive_ages = [
        0,
        0.0,
        0.0001,
        0.2,
        1.0,
        1,
        10.0,
        25.052,
        50,
        100
    ]

negative_ages = [
        -1000,
        - 1.0,
        - 0.1,
        100,
        None,
        True,
        math.pi,
        'one',
        '',
        [100],
        {1: 10},
        dict(),
        list()
    ]


def generate_valid_bears(amount):
    result = list()
    for c in range(amount):
        result.append({
            "bear_type": random.choice(['POLAR', 'BROWN', 'BLACK', 'GUMMY']),
            "bear_name": ''.join(random.choice(string.ascii_uppercase) for _ in range(5)),
            "bear_age": random.uniform(0.0, 50.0)  # because bears cannot living more than 50 years
        })
    return result


def is_not_single(bears):
    if len(bears) != 1:
        return f"Incorrect length of response! Expected 1, got {len(bears)}"
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
    assert not any([is_not_single(bears), errors]), 'errors occurred:\n{}'.format('\n'.join(errors))


@pytest.mark.parametrize("bear_type", negative_types)
@pytest.mark.usefixtures('no_bears')
def test_negative_type_create_single_bear(api, bear_type):
    insert_bear = {'bear_type': bear_type, 'bear_name': 'MIKHAIL', 'bear_age': 17.5}
    api.create_bear(insert_bear)
    bears = api.get_all_bears()
    errors = list()
    if len(bears) > 0:
        errors.append(f'Bear {insert_bear} unexpectedly added to db')
    assert not errors, 'errors occurred:\n{}'.format('\n'.join(errors))


@pytest.mark.parametrize("name", negative_names)
@pytest.mark.usefixtures('no_bears')
def test_negative_type_create_single_bear(api, name):
    insert_bear = {'bear_type': 'POLAR', 'bear_name': name, 'bear_age': 17.5}
    api.create_bear(insert_bear)
    bears = api.get_all_bears()
    errors = list()
    if len(bears) > 0:
        errors.append(f'Bear {insert_bear} unexpectedly added to db')
    assert not errors, 'errors occurred:\n{}'.format('\n'.join(errors))


@pytest.mark.parametrize("age", negative_ages)
@pytest.mark.usefixtures('no_bears')
def test_negative_type_create_single_bear(api, age):
    insert_bear = {'bear_type': 'POLAR', 'bear_name': 'MIKHAIL', 'bear_age': age}
    api.create_bear(insert_bear)
    bears = api.get_all_bears()
    errors = list()
    if len(bears) > 0:
        errors.append(f'Bear {insert_bear} unexpectedly added to db')
    assert not errors, 'errors occurred:\n{}'.format('\n'.join(errors))


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
    assert not errors, 'errors occurred:\n{}'.format('\n'.join(errors))


@pytest.mark.usefixtures('no_bears')
def test_less_params(api):
    for key in ['bear_type', 'bear_name', 'bear_age']:
        bear = generate_valid_bears(1)[0]
        bear.pop(key)
        api.create_bear(bear)
        bears = api.get_all_bears()
        assert not bears, f'Bear created incorrectly without important parameter {key}'


# Probably we should ignore unknown fields in request json and if json have all necessary fields - system should
# creates bear. If not - this test invalid
@pytest.mark.usefixtures('no_bears')
def test_more_params(api):
    bear = generate_valid_bears(1)[0]
    bear.update({"bear_mood": "happy"})
    api.create_bear(bear)
    bears = api.get_all_bears()
    bear.pop("bear_mood")
    errors = is_invalid(bear, bears[0])
    assert not any([is_not_single(bears), errors]), 'errors occurred:\n{}'.format('\n'.join(errors))


if __name__ == '__main__':
    pytest.main(['-qq'])
