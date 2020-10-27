import pytest
from api_helper import BearAPI


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
