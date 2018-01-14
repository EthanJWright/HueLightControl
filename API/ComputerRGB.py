class ComputerRGB():
    def __init__(self, _config):
        self.config = _config

    def handle_request(json):
        comp_pi = self.config.read('Computer Pi')
        url = comp_pi + ':5000/'
        payload = json
        response = requests.post(url, json=payload).json()
        print response
        return response
