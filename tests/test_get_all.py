import pytest


@pytest.mark.usefixtures('no_bears')
def test_get_all_no_bears(api):
    bears = api.get_all_bears()
    assert len(bears) == 0, f'There is incorrect amount of bears returned by read all bears method: {len(bears)}'


@pytest.mark.usefixtures('single_bear')
def test_get_all_single_bear(api):
    bears = api.get_all_bears()
    assert len(bears) == 1, f'There is incorrect amount of bears returned by read all bears method: {len(bears)}'


@pytest.mark.usefixtures('many_bears')
def test_get_all_many_bears(api):
    bears = api.get_all_bears()
    assert len(bears) == 50, f'There is incorrect amount of bears returned by read all bears method: {len(bears)}'
