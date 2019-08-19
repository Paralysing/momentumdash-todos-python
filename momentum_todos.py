from datetime import datetime
import requests
import uuid

class MomentumTodos:
    def __init__(self, bearer_token, client_uuid=str(uuid.uuid1()), client_user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36' todo_list_id='1-inbox'):
        self.bearer_token = bearer_token
        self.todo_list_id = todo_list_id
        self.client_uuid = client_uuid
        self.client_headers = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'authorization': self.bearer_token,
            'content-type': 'application/json',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'cross-site',
            'origin': 'chrome-extension://laookkfknpbbblfpciffpaejjkokdgca',
            'user-agent': client_user_agent,
            'x-momentum-clientdate': 0,
            'x-momentum-clientid': self.client_uuid,
            'x-momentum-version': '1.11.8'
        }

    def momentum_api_req(self, method, url, json={}):
        self.client_headers['x-momentum-clientdate'] = self.get_datetime(for_headers=True)
        r = None
        if method == 'get':
            r = requests.get(url=url, headers=self.client_headers, timeout=10)
        elif method == 'post':
            r = requests.post(url=url, headers=self.client_headers, json=json, timeout=10)
        elif method == 'patch':
            r = requests.patch(url=url, headers=self.client_headers, json=json, timeout=10)
        return r

    def set_todo_list_id(self, todo_list_id):
        self.todo_list_id = todo_list_id

    def get_datetime(self, for_headers=False):
        if for_headers:
            return str(datetime.now()).split('.')[0].replace(' ', 'T')
        return str(datetime.utcnow()).replace(' ', 'T')[:-3] + 'Z'

    def get_todo_lists(self):
        r = self.momentum_api_req(method='get', url='https://api.momentumdash.com/todos/lists?provider_id=1&project_id=1')
        return r.json()

    def get_todo_list_items(self):
        r = self.momentum_api_req(method='get', url='https://api.momentumdash.com/todos?listId=' + self.todo_list_id)
        return r.json()

    def add_item_to_todo_list(self, title):
        r = self.momentum_api_req(
            method = 'post', 
            url = 'https://api.momentumdash.com/todos', 
            json = {
                'archive': False,
                'archivedDate': None,
                'completedDate': None,
                'createdDate': self.get_datetime(for_headers=False),
                'deleted': False,
                'deletedDate': None,
                'done': False,
                'homeListId': self.todo_list_id,
                'listId': self.todo_list_id,
                'serverSetId': False,
                'title': title,
                'unsyncable': False
            }
        )
        return r.json()['id']

    def finish_item_in_todo_list(self, item_id):
        r = self.momentum_api_req(
            method = 'patch', 
            url = 'https://api.momentumdash.com/todos/' + item_id, 
            json = {
                'completedDate': self.get_datetime(for_headers=False),
                'done': True,
                'projectId': '1',
                'providerId': '1'
            }
        )

    def delete_item_in_todo_list(self, item_id):
        r = self.momentum_api_req(
            method = 'patch', 
            url = 'https://api.momentumdash.com/todos/' + item_id, 
            json = {
                'deletedDate': self.get_datetime(for_headers=False),
                'deleted': True,
                'projectId': '1',
                'providerId': '1'
            }
        )
