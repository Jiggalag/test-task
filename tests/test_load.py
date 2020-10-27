import datetime
import pytest
import random
import string


def generate_valid_bears(amount):
    result = list()
    for c in range(amount):
        result.append({
            "bear_type": random.choice(['POLAR', 'BROWN', 'BLACK', 'GUMMY']),
            "bear_name": ''.join(random.choice(string.ascii_uppercase) for _ in range(5)),
            "bear_age": random.uniform(0.0, 50.0)  # because bears cannot living more than 50 years
        })
    return result


@pytest.mark.usefixtures('no_bears')
@pytest.mark.skip(reason='It is dummy load test should be implemented with multithreading')
def test_load(api):
    start = datetime.datetime.now()
    # 1 mln - it's a empiric infinum of bear's amount on Alaska. Now there are about 100 thousand bears.
    bears = generate_valid_bears(100000)
    for bear in bears:
        api.create_bear(bear)
    bears = api.get_all_bears()
    finished_in = datetime.datetime.now() - start
    print(f'Load test finished in {datetime.timedelta(seconds=round(finished_in))} minutes')
    assert len(bears) == 10000000, f'Generated 1 mln bears, but loaded only {len(bears)}'
