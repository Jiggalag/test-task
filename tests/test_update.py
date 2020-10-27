import pytest

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
        0.0001,
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


def is_invalid(request_bear, result):
    errors = list()
    if type(result) == dict:
        result.pop('bear_id')
        if result != request_bear:
            for item in ['bear_type', 'bear_name', 'bear_age']:
                if result.get(item) != request_bear.get(item):
                    errors.append(f'Incorrect {item}! Expected: {request_bear.get(item)}, got: {result.get(item)}')
                result.pop(item)
                request_bear.pop(item)
            if result:
                errors.append(f'There is excess keys founded in result: {result.keys()}')
    else:
        errors.append(f'Incorrect type of result: {type(result)}, result: {result}')
    return errors, 'errors occurred:\n{}'.format('\n'.join(errors))


@pytest.mark.parametrize("bear_type", positive_types)
@pytest.mark.parametrize("name", positive_names)
@pytest.mark.parametrize("age", positive_ages)
@pytest.mark.usefixtures('single_bear')
@pytest.mark.xfail
def test_positive_update(api, bear_type, name, age):
    bear_id = api.get_all_bears()[0].get('bear_id')
    update_bear = {'bear_type': bear_type, 'bear_name': name, 'bear_age': age}
    api.update_specific_bear(bear_id, update_bear)
    updated_bear = api.get_specific_bear(bear_id)
    errors = is_invalid(update_bear, updated_bear)
    assert not errors, 'errors occurred:\n{}'.format('\n'.join(errors))


@pytest.mark.parametrize("bear_type", negative_types)
@pytest.mark.parametrize("name", negative_names)
@pytest.mark.parametrize("age", negative_ages)
@pytest.mark.usefixtures('single_bear')
@pytest.mark.xfail
def test_negative_update(api, bear_type, name, age):
    bear_id = api.get_all_bears()[0].get('bear_id')
    update_bear = {'bear_type': bear_type, 'bear_name': name, 'bear_age': age}
    status_code = api.update_specific_bear(bear_id, update_bear)
    errors = list()
    if status_code != 200:
        errors.append(f'Update request returned code {status_code}')
    updated_bear = api.get_specific_bear(bear_id)
    errors.append(is_invalid(update_bear, updated_bear))
    assert not errors, 'errors occurred:\n{}'.format('\n'.join(errors))


@pytest.mark.usefixtures('single_bear')
@pytest.mark.xfail
def test_update_mixed_values(api):
    # try to simultaneously update two parameters - first with valid value, second - with invalid
    bear_id = api.get_all_bears()[0].get('bear_id')
    update_bear = {'bear_type': 'INCORRECT', 'bear_name': 'MIKHAIL', 'bear_age': 17.5}
    status_code = api.update_specific_bear(bear_id, update_bear)
    errors = list()
    if status_code != 200:
        errors.append(f'Update request returned code {status_code}')
    updated_bear = api.get_specific_bear(bear_id)
    errors.append(is_invalid(update_bear, updated_bear))
    assert not errors, 'errors occurred:\n{}'.format('\n'.join(errors))


@pytest.mark.usefixtures('single_bear')
@pytest.mark.xfail
def test_update_not_existed_param(api):
    bear_id = api.get_all_bears()[0].get('bear_id')
    update_bear = {'not_existed_param': 'test'}
    before_update = api.get_specific_bear(bear_id)
    status_code = api.update_specific_bear(bear_id, update_bear)
    errors = list()
    if status_code != 200:
        errors.append(f'Update request returned code {status_code}')
    after_update = api.get_specific_bear(bear_id)
    if before_update != after_update:
        errors.append(f'Seems bear update by request with not existed key. '
                      f'Before update: {before_update}, after update: {after_update}')
    assert not errors, 'errors occurred:\n{}'.format('\n'.join(errors))


# I think system should ignore not existed keys and update only
@pytest.mark.usefixtures('single_bear')
@pytest.mark.xfail
def test_update_existed_and_not_existed_key(api):
    bear_id = api.get_all_bears()[0].get('bear_id')
    update_bear = {'not_existed_param': 'test'}
    before_update = api.get_specific_bear(bear_id)
    status_code = api.update_specific_bear(bear_id, update_bear)
    errors = list()
    if status_code != 200:
        errors.append(f'Update request returned code {status_code}')
    after_update = api.get_specific_bear(bear_id)
    if before_update != after_update:
        errors.append(f'Seems bear update by request with not existed key. '
                      f'Before update: {before_update}, after update: {after_update}')
    assert not errors, 'errors occurred:\n{}'.format('\n'.join(errors))


@pytest.mark.usefixtures('two_bears')
@pytest.mark.xfail
def test_update_bear_to_make_identical(api):
    bears = api.get_all_bears()
    bear_id = bears[1].get('bear_id')
    for item in ['bear_name', 'bear_type', 'bear_age']:
        bears[1].update({item: bears[0].get(item)})
    status_code = api.update_specific_bear(bear_id, bears[1])
    errors = list()
    if status_code != 200:
        errors.append(f'Update request returned code {status_code}')
    assert not errors, 'errors occurred:\n{}'.format('\n'.join(errors))


if __name__ == '__main__':
    pytest.main(['-qq'])
