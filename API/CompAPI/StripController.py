from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
import LED_controller
import time
import json

hostIP="192.168.1.8"
app = FlaskAPI(__name__)
led = LED_controller.rgb([5,4,12])

@app.route("/", methods=['GET', 'POST'])
def get_request():
    if request.method == 'POST':
        return_val = {}
        payload = request.get_json(silent=True)
        if(payload.has_key('rgb')):
            led.set(payload['rgb'])
            print payload['rgb']
            return_val = {'value' : 'success'}
        if(payload.has_key('on') and not payload['on']):
            led.set([0,0,0])
        return json.dumps(return_val)
    
if __name__ == "__main__":
    app.run(host=hostIP)
led.end
