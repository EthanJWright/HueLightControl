import requests
import json

url = 'http://73.78.132.90:5000/'
payload = {
        'action' : 'hue',
        'params' : {
            'group' : 'fan',
            'on' : True,
            'rgb' : '.0,.6,.9',
            'brightness' : '100'
            }
        }
response = requests.post(url,json=payload).json()
print response
