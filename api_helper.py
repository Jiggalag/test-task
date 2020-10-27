import json
import requests


class BearAPI:
    def __init__(self, url, port):
        self.url = f'http://{url}:{port}'

    def __get_info__(self):
        return requests.get(self.url + '/info').text

    def create_bear(self, bear):
        # POST			/bear - create
        # Example of ber json: {"bear_type":"BLACK","bear_name":"mikhail","bear_age":17.5}
        # Available types for bears are: POLAR, BROWN, BLACK and GUMMY.
        return requests.post(self.url + '/bear', json=bear).status_code

    def get_all_bears(self):
        # GET			/bear - read all bears
        return json.loads(requests.get(self.url + '/bear').text)

    def get_specific_bear(self, bear_id):
        # GET			/bear/:id - read specific bear
        raw_result = requests.get(self.url + f'/bear/:{bear_id}').text
        try:
            return json.loads(raw_result)
        except json.decoder.JSONDecodeError as e:
            print(e)
            return raw_result

    # use this function as a workaround until developers fixed getting specific bear by id
    def get_specific_bear_hack(self, bear_id):
        raw_result = requests.get(self.url + '/bear').text
        try:
            result = json.loads(raw_result)
            for item in result:
                if int(item.get('bear_id')) == bear_id:
                    return item
            return {}
        except json.decoder.JSONDecodeError as e:
            print(e)
            return raw_result

    def update_specific_bear(self, bear_id, bear):
        # PUT			/bear/:id - update specific bear
        return requests.put(self.url + f'/bear/:{bear_id}', json=bear).status_code

    def delete_all_bears(self):
        # DELETE			/bear - delete all bears
        return requests.delete(self.url + '/bear').status_code

    def delete_specific_bear(self, bear_id):
        # DELETE			/bear/:id - delete specific bear
        return requests.delete(self.url + f'/bear/:{bear_id}').status_code
