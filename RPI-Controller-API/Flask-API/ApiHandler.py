import requests


class ApiHandler():
    def __init__(self, _ip):
        self.ip = _ip

    def handle_request(self, json):
        url = 'http://' + self.ip + ':5000/'
        payload = json
        response = requests.post(url, json=payload).json()
        print response
        return response
