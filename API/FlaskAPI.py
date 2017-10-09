from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
import HueController
from colour import Color
import simplejson

app = FlaskAPI(__name__)

hue = HueController.hue_rgb("192.168.1.2")

def set_rgb(rgb):
    rgb = rgb.split(',')
    rgb = map(float, rgb)
    hue.rgb_set(rgb)

def hue_on(state):
    hue.on(state)

def set_brightness(brightness):
    print brightness
    hue.brightness(int(float(brightness) * 2.54))

def handle_hue(payload):
    try:
        hue.set_group(payload['group'])
    except:
        return failed("couldn't get group")
    if(payload.has_key('brightness')):
        set_brightness(payload['brightness'])
    if(payload.has_key('rgb')):
        try:
            set_rgb(payload['rgb'])
        except:
            return failed("couldn't change rgb")
    if(payload.has_key('on')):
        hue_on(payload['on'])
    return {'API Status' : 'suceeded'}

def failed(result):
    return {
            'api result' : result
            }

@app.route("/", methods=['GET', 'POST'])
def get_request():
    if request.method == 'POST':
#        action = str(request.data.get('action', ''))
        payload = request.get_json(silent=True)
        if(payload['action'] == 'hue'):
            return handle_hue(payload['params']);
        else:
            return failed("couldn't get params")

if __name__ == "__main__":
    app.run(debug=True, host='192.168.1.3')
