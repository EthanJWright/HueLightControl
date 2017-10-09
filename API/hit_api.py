import requests
import json

url = 'http://73.78.132.90:5000/'
payload = {
        'action' : 'hue',
        'params' : {
            'group' : 'fan',
            'on' : True,
            'change' : 'on',
            'rgb' : '.3,.3,.3'
            }
        }
response = requests.post(url,json=payload).json()
print response
