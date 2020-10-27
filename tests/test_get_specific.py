import pytest


@pytest.mark.usefixtures('single_bear')
@pytest.mark.xfail
def test_get_existed_bear(api):
    bear_id = api.get_all_bears()[0].get('bear_id')
    hacked_bear = api.get_specific_bear_hack(bear_id)
    bear = api.get_specific_bear(bear_id)
    assert bear == hacked_bear, f'Seems like getting specific bear method work incorrectly! ' \
                                f'Expected bear: {hacked_bear}, actual: {bear}'


@pytest.mark.usefixtures('two_bears')
def test_get_previously_deleted_bear(api):
    bear_id = api.get_all_bears()[0].get('bear_id')
    errors = list()
    status_code = api.delete_specific_bear(bear_id)
    if status_code != 200:
        errors.append(f'Delete-bear method returned status_code {status_code}')
    bears = api.get_all_bears()
    if len(bears) != 1:
        errors.append(f'There is not one bear remained in db. Actual bear amount: {len(bears)}')
    status_code = api.delete_specific_bear(bear_id)
    if status_code == 200:
        errors.append('Delete-bear method returned status_code 200, despite bear already should be deleted')
    assert errors, 'errors occurred:\n{}'.format('\n'.join(errors))


@pytest.mark.usefixtures('single_bear')
def test_get_never_existent_bear(api):
    bear_id = api.get_all_bears()[0].get('bear_id')
    errors = list()
    bear = api.get_specific_bear(int(bear_id) + 1)
    if bear != 'EMPTY':
        errors.append(f'There is incorrect bear got: {bear}')
    assert not errors, 'errors occurred:\n{}'.format('\n'.join(errors))


@pytest.mark.usefixtures('single_bear')
def test_getting_by_non_id(api):
    bear = api.get_specific_bear('qwe')
    assert bear == 'EMPTY', 'Incorrect bear got by knowingly invalid id'
