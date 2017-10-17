from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
import HueController
from colour import Color
import simplejson
import datetime
import time
import ConfigParser

config = ConfigParser.ConfigParser()
config.read('api.properties')
hueIP = config.get('Hue', 'ip')
hostIP=config.get('Host', 'ip')
app = FlaskAPI(__name__)
hue = HueController.hue_rgb(hueIP)
hue.on(False)

def logger(information):
    f = open('api.log', 'a+')
    ts = time.time()
    f.write(information +  "  Timestamp: " + str(datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))  + '\n')
    f.close

def set_hue():
    hue = HueController.hue_rgb(hueIP)


def set_rgb(rgb):
    rgb = rgb.split(',')
    rgb = map(float, rgb)
    hue.rgb_set(rgb)

def hue_on(state):
    print state
    if(type(state) is str or type(state) is unicode):
        if(state == 'True' or state == 'true'):
            hue.on(True)
        if(state == 'False' or state == 'false'):
            hue.on(False)
    else:
        hue.on(state)

def set_brightness(brightness):
    hue.brightness(int(float(brightness) * 2.54))

def handle_transition(payload):
    hue.transition(payload)

def handle_hue(payload):
    print 'in handle hue'
    set_hue()
    try:
        hue.set_group(payload['group'])
    except:
        return failed("couldn't get group", payload)
    if(payload.has_key('on')):
        # If turning lights on, we need to turn on before anything else
        if(payload['on'] or payload['on'] == 'true' or payload['on'] == 'True'):
            hue_on(payload['on'])
    if(payload.has_key('transitiontime')):
        print "transition"
        handle_transition(payload)
    if(payload.has_key('brightness')):
        set_brightness(payload['brightness'])
    if(payload.has_key('rgb')):
        try:
            set_rgb(payload['rgb'])
        except:
            return failed("couldn't change rgb", payload)
    if(payload.has_key('on')):
        # If turning off, we need to turn off last
        if(not payload['on'] or payload['on'] == 'False' or payload['on'] == 'false'):
            hue_on(payload['on'])
    return hue_suceeded()

def handle_check_hue(payload):
    try:
        hue.set_group(payload['group'])
        print hue.get_group_status()
        return hue_suceeded()
    except:
        return failed("couldn't get group", payload)

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
    return { 'hue result' : hue.get_all(), 'ip_result' : get_ip() }
            

def failed(result, payload):
    logger(result + str(payload))
    return {
            'api result' : result
            }

@app.route("/", methods=['GET', 'POST'])
def get_request():
    if request.method == 'POST':
        payload = request.get_json(silent=True)
        if(payload.has_key('hue')):
            return handle_hue(payload['hue']);
        if(payload.has_key('check hue')):
            try:  
                return handle_check_hue(payload['check hue'])
            except: 
                return failed("Couldn't get group", payload)
        else:
            return failed("couldn't get params", payload)

if __name__ == "__main__":
    app.run(debug=True,host=hostIP)
