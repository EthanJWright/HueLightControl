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
        if(payload.has_key('hue')):
            return_val['hue_result'] = hueApi.handle_hue(payload['hue'])
        if(payload.has_key('computer')):
            comp_ip = config.get('RPI LED, 'ip'')
            comp = ApiHandler.ApiHandler(comp_ip)
            return_val['computer_result'] = comp.handle_request(payload['computer'])
        return_val['ip_result'] = 'none'
        return json.dumps(return_val)

if __name__ == "__main__":
    app.run(host=hostIP)
