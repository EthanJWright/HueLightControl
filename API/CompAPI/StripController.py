from flask import request, url_for
from flask_api import FlaskAPI, status, exceptions
import LED_controller
import time
hostIP="192.168.1.15"
app = FlaskAPI(__name__)
led = LED_controller.rgb([16, 20, 21])

@app.route("/", methods=['GET', 'POST'])
def get_request():
    if request.method == 'POST':
        return_val = {}
        payload = request.get_json(silent=True)
        if(payload.has_key('rgb')):
            print payload['rgb']
if __name__ == "__main__":
    app.run(host=hostIP)
led.end
