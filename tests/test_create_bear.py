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
def test_create_single_bear(api, bear_type, name, age):
    insert_bear = {'bear_type': bear_type, 'bear_name': name, 'bear_age': age}
    api.create_bear(insert_bear)
    bears = api.get_all_bears()
    errors = list()
    assert not any([is_not_single(bears), is_invalid(insert_bear, bears[0])]), \
        'errors occured:\n{}'.format('\n'.join(errors))


if __name__ == '__main__':
    pytest.main(['-qq'])
