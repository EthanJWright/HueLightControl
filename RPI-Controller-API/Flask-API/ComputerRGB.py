import requests
import ConfigParser


class ComputerRGB():
    def __init__(self, _config):
        self.config = _config

    def handle_request(self, json):
        comp_pi = self.config.get('RPI LED', 'ip')
        print(comp_pi)
        url = 'http://' + comp_pi + ':5000/'
        payload = json
        response = requests.post(url, json=payload).json()
        print response
        return response
