import pytest


@pytest.mark.usefixtures('single_bear')
def test_delete_last_bear(api):
    bear_id = api.get_all_bears()[0].get('bear_id')
    errors = list()
    status_code = api.delete_specific_bear(bear_id)
    if status_code != 200:
        errors.append(f'Delete request returned code {status_code}, despite we can delete this bear!')
    bears = api.get_all_bears()
    if len(bears) > 0:
        errors.append('Last bear not deleted!')
    assert errors, 'errors occurred:\n{}'.format('\n'.join(errors))


@pytest.mark.usefixtures('two_bears')
def test_repeated_delete_bear(api):
    bear_id = api.get_all_bears()[0].get('bear_id')
    errors = list()
    status_code = api.delete_specific_bear(bear_id)
    if status_code != 200:
        errors.append(f'Delete request returned code {status_code}, despite we can delete this bear')
    bears = api.get_all_bears()
    if len(bears) != 1:
        errors.append(f'Penultimate bear not deleted! Amount of bears in db {len(bears)}')
    status_code = api.delete_specific_bear(bear_id)
    if status_code == 200:
        errors.append(f'Delete request returned code {status_code}, but this bear already deleted')
    assert errors, 'errors occurred:\n{}'.format('\n'.join(errors))


@pytest.mark.usefixtures('single_bear')
def test_delete_not_existed_bear(api):
    bear_id = api.get_all_bears()[0].get('bear_id')
    errors = list()
    status_code = api.delete_specific_bear(int(bear_id) + 1)
    if status_code == 200:
        errors.append(f'Delete request returned code {status_code}, despite bear should not be deleted')
    bears = api.get_all_bears()
    if len(bears) != 1:
        errors.append(f'There is incorrect amount of bears after attempt to delete non-existent bear: {len(bears)}')
    assert errors, 'errors occurred:\n{}'.format('\n'.join(errors))
