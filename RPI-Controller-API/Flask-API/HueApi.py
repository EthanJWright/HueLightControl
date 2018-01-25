import HueController
from colour import Color
import simplejson
import datetime
import time
import ConfigParser

class HueApi():
    def __init__(self):
        self.config = ConfigParser.ConfigParser()
        self.config.read('iot.properties')
        self.hueIP = self.config.get('Hue', 'ip')
        self.hue = HueController.hue_rgb(self.hueIP)
        self.hue.on(False)

    def set_rgb(self, rgb):
        rgb = rgb.split(',')
        rgb = map(float, rgb)
        hue.rgb_set(rgb)


    def hue_on(self, state):
        if(type(state) is str or type(state) is unicode):
            if(state == 'True' or state == 'true'):
                self.hue.on(True)
            if(state == 'False' or state == 'false'):
                self.hue.on(False)
        else:
            self.hue.on(state)

    def set_brightness(self, brightness):
        self.hue.brightness(int(float(brightness) * 2.54))

    def handle_transition(self, payload):
        self.hue.transition(payload)

    def handle_hue(self, payload):
        try:
            self.hue.set_group(payload['group'])
        except:
            return False
        if(payload.has_key('on')):
            # If turning lights on, we need to turn on before anything else
            if(payload['on'] or payload['on'] == 'true' or payload['on'] == 'True'):
                self.hue_on(payload['on'])
        if(payload.has_key('transitiontime')):
            self.handle_transition(payload)
        if(payload.has_key('brightness')):
            self.set_brightness(payload['brightness'])
        if(payload.has_key('rgb')):
            try:
                self.set_rgb(payload['rgb'])
            except:
                return False
        if(payload.has_key('on')):
            # If turning off, we need to turn off last
            if(not payload['on'] or payload['on'] == 'False' or payload['on'] == 'false'):
                self.hue_on(payload['on'])
        return self.hue_suceeded()

    def hue_suceeded(self):
        return self.hue.get_all()

