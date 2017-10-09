import requests
import json

url = 'http://73.78.132.90:5000/'
payload = {
        'action' : 'hue',
        'params' : {
            'group' : 'fan',
            'on' : True,
            'rgb' : '.3,.0,.9',
            'brightness' : '100',
            'transitiontime' : '20'
            }
        }
response = requests.post(url,json=payload).json()
print response
