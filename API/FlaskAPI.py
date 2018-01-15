from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
import HueController
from colour import Color
import simplejson
import datetime
import time
import ConfigParser
import HueApi
import json
import ComputerRGB

config = ConfigParser.ConfigParser()
config.read('api.properties')
hostIP=config.get('Host', 'ip')
hueApi = HueApi.HueApi()

app = FlaskAPI(__name__)

def logger(information):
    pass
#    f = open('api.log', 'a+')
#    ts = time.time()
#    f.write(information +  "  Timestamp: " + str(datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))  + '\n')
#    f.close

def get_ip():
    ip_stuff = {}
    riv_set = False
    ethan_set = False
    # Check results from nmap scan
    with open('/home/pi/nmap_results.txt') as f:
        content = f.readlines()
        content = [x.strip() for x in content]
        for element in content:
            if('192.168.1.6' in str(element)):
                ethan_set = True
        for element in content:
            if('192.168.1.7' in str(element)):
                riv_set = True
        ip_stuff['Ethan'] = ethan_set
        ip_stuff['River'] = riv_set

    return ip_stuff


def hue_suceeded():
    return { 'hue_result' : hue.get_all(), 'ip_result' : get_ip() }
            

def failed(result, payload):
    logger(result + str(payload))
    return {
            'hue_result' : result
            }

@app.route("/", methods=['GET', 'POST'])
def get_request():
    if request.method == 'POST':
        return_val = {}
        payload = request.get_json(silent=True)
        if(payload.has_key('hue')):
            return_val['hue_result'] = hueApi.handle_hue(payload['hue'])
        if(payload.has_key('computer')):
            comp = ComputerRGB.ComputerRGB(config)
            return_val['computer_result'] = comp.handle_request(payload['computer'])
        return_val['ip_result'] = get_ip()
        return json.dumps(return_val)

if __name__ == "__main__":
    app.run(host=hostIP)
