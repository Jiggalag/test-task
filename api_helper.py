import json
import requests


class BearAPI:
    def __init__(self, url, port):
        self.url = f'http://{url}:{port}'

    def __get_info__(self):
        return json.loads(requests.get(self.url + '/info').text)

    def create_bear(self, bear):
        # POST			/bear - create
        # Example of ber json: {"bear_type":"BLACK","bear_name":"mikhail","bear_age":17.5}
        # Available types for bears are: POLAR, BROWN, BLACK and GUMMY.
        requests.post(self.url + '/bear', json=bear)

    def get_all_bears(self):
        # GET			/bear - read all bears
        return json.loads(requests.get(self.url + '/bear').text)

    def get_specific_bear(self, bear_id):
        # GET			/bear/:id - read specific bear
        return json.loads(requests.get(self.url + f'/bear/:{bear_id}').text)

    def update_specific_bear(self, bear_id, bear):
        # PUT			/bear/:id - update specific bear
        requests.put(self.url + f'/bear/:{bear_id}', json=bear)

    def delete_all_bears(self):
        # DELETE			/bear - delete all bears
        requests.delete(self.url + '/bear')

    def delete_specific_bear(self, bear_id):
        # DELETE			/bear/:id - delete specific bear
        requests.delete(self.url + f'/bear/:{bear_id}')
