import requests
import json

url = 'http://127.0.0.1:5000/'
payload = {
        'hello' : {
            'name' : 'world',
            'data' : True,
            'do_something' : 'use data'
            },
        'more data' : 'here'
        }
response = requests.post(url,json=payload).json()
print response
