import requests
import json
import time

url = 'http://73.78.132.90:5000/'


payload_one = {
        'hue' :  {
            'group' : 'fan',
            'on' : True,
            'rgb' : '.9,.9,.3',
            'brightness' : '100'
            }
        }
payload_two = {
        'hue' :  {
            'group' : 'fan',
            'on' : False,
            'rgb' : '.9,.9,.3',
            'brightness' : '100'
            }
        }

for i in range(0, 30):
    response = requests.post(url,json=payload_one).json()
    print response
    time.sleep(3)
    response = requests.post(url,json=payload_two).json()
    print response
    time.sleep(3)

response = requests.post(url,json=payload_one).json()
print response
