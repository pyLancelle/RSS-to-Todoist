import requests
from typing import Dict, List, Any
import json

class TodoistAuth:
    def __init__(self, personal_access_token):
        self.personal_access_token = personal_access_token
        self.headers = {'Authorization': f'Bearer {self.personal_access_token}'}

class TodoistApi:
    BASE_URL = 'https://api.todoist.com/rest/v2/'

    def __init__(self, auth: TodoistAuth):
        self.auth = auth

    def make_request(self, method, endpoint, params: Dict = None, data: Dict = None):
        url = f'{self.BASE_URL}{endpoint}'

        try:
            if method == 'get':
                response = requests.get(url, headers=self.auth.headers, params=params, timeout=20)
            elif method == 'post':
                response = requests.post(url, headers=self.auth.headers, json=data, timeout=20)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            if response.status_code:
                pass
                # print(f'Success !')
            return response.json()
        
        except requests.RequestException as e:
            print(f"API request failed: {e}")
            return {}

class TaskManager:
    def __init__(self, api: TodoistApi):
        self.api = api

    def get_all_projects(self):
        return self.api.make_request(method='get', endpoint='projects')
    
    def get_all_tasks(self, section_id = None):
        return self.api.make_request(method='get', endpoint='tasks', params={'section_id': section_id})
    
    def get_all_sections(self, project_id = None):
        return self.api.make_request(method='get', endpoint='sections', params={'project_id' : project_id})
    
    def add_section(self, project_id, section_name):
        all_sections = self.get_all_sections(project_id)
        for section in all_sections:
            if section['name'] == section_name:
                print(f'Section {section_name} already exists\n')
                return {'id' : section['id']}
        return self.api.make_request(method='post', endpoint='sections', data={'name': section_name, 'project_id': project_id})

    def add_task(self, content):
        return self.api.make_request(method='post', endpoint='tasks', data=content)