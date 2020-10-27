import pytest


@pytest.mark.usefixtures('no_bears')
def test_delete_all_from_empty_db(api):
    status_code = api.delete_all_bears()
    assert status_code == 200, 'Status code is {} when we try to delete bears from empty db'


@pytest.mark.usefixtures('single_bear')
def test_delete_all_single_bear(api):
    status_code = api.delete_all_bears()
    errors = list()
    if status_code != 200:
        errors.append(f'Delete request returned code {status_code}, despite we can delete single bear')
    bears = api.get_all_bears()
    if len(bears) != 0:
        errors.append(f'After deleting bear still alive! Amount of bears after deleting {len(bears)}')
    assert not errors, 'errors occurred:\n{}'.format('\n'.join(errors))


@pytest.mark.usefixtures('many_bears')
def test_delete_many_bears(api):
    status_code = api.delete_all_bears()
    errors = list()
    if status_code != 200:
        errors.append(f'Delete request returned code {status_code}, despite we can delete many bears')
    bears = api.get_all_bears()
    if len(bears) != 0:
        errors.append(f'After deleting some bears still alive! Amount of bears after deleting {len(bears)}')
    assert not errors, 'errors occurred:\n{}'.format('\n'.join(errors))
