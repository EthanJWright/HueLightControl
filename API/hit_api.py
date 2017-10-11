import requests
import json

url = 'http://73.78.132.90:5000/'
payload = {
        'hue' : {
            'group' : 'fan',
            'on' : True,
            'rgb' : '.6,.6,.1',
            'brightness' : '100',
            'transitiontime' : '20'
            }
        }

response = requests.post(url,json=payload).json()
print response
