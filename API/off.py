import requests
import json

url = 'http://73.78.132.90:5000/'
payload = {
        'hue' :  {
            'group' : 'fan',
            'on' : False,
            'rgb' : '.9,.9,.3',
            'brightness' : '100'
            }
        }
response = requests.post(url,json=payload).json()
print response
