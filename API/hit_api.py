import requests
import json

url = 'http://73.78.132.90:5000/'
payload = {
        'hue' : {
            'group' : 'fan',
            'on' : True,
            'brightness' : '100',
            'transitiontime' : '20'
            }
        }

payload = {
        'computer' : {
            'brightness' : 100,
            'rgb' : [255, 0, 255],
            'on' : True 
            }
        }
response = requests.post(url,json=payload).json()
print response

