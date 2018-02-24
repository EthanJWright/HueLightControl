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
import ApiHandler
import nmap

config = ConfigParser.ConfigParser()
config.read('iot.properties')
hostIP=config.get('Controller', 'ip')
hostIP='0.0.0.0'
hueApi = HueApi.HueApi()

app = FlaskAPI(__name__)

def logger(information):
    pass
#    f = open('api.log', 'a+')
#    ts = time.time()
#    f.write(information +  "  Timestamp: " + str(datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))  + '\n')
#    f.close
def check_if_home(nm):
    riv, ethan = False, False
    for h in nm.all_hosts():
        if 'mac' in nm[h]['addresses']:
            if(nm[h]['addresses']['mac'] == 'EC:9B:F3:EE:51:4B'):
                riv = True
            if(nm[h]['addresses']['mac'] == 'B4:F1:DA:EA:28:DB'):
                ethan = True
    return riv,ethan


def check_home():
    nm = nmap.PortScanner()
    nm.scan(hosts='192.168.1.1/24', arguments='-n -sP')
    nm.command_line()

    report = [' is not home.', ' is home.']
    for i in range(0,6):
        riv,ethan = check_if_home(nm)
        if(riv and ethan):
            print("Ethan and River are Home.")
            return "Ethan and River are Home."

    return "Ethan" + report[int(ethan)] + "\n" +"River" + report[int(riv)]





def hue_suceeded():
    return { 'hue_result' : hue.get_all(), 'ip_result' : 'none' }
            

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
        print(payload)
        if(payload.has_key('hue')):
            return_val['hue_result'] = hueApi.handle_hue(payload['hue'])
        if(payload.has_key('computer')):
            ip = config.get('RPI LED Computer', 'ip')
            comp = ApiHandler.ApiHandler(ip)
            return_val['computer_result'] = comp.handle_request(payload['computer'])
        if(payload.has_key('door')):
            ip = config.get('RPI LED Door', 'ip')
            api = ApiHandler.ApiHandler(ip)
            return_val['door_result'] = api.handle_request(payload['door'])
        if(payload.has_key('check_home')):
            return_val['check_home'] = check_home()
        print(json.dumps(return_val))
        return json.dumps(return_val)

if __name__ == "__main__":
    app.run(host=hostIP)
