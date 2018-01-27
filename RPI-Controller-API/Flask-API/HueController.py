#!/usr/bin/python
import random
import collections
import logging
from phue import Bridge
logging.basicConfig()

class hue_rgb():
    def __init__(self, _ip):
        self.Point = collections.namedtuple('Point', ['x', 'y'])
        self.b = Bridge(_ip)
        self.b.connect()
        self.b.get_api()
        self.group = None
        self.lights = []

    def convert_rgb(self, red, green, blue):
        red = red / 255
        blue = blue / 255
        green = green / 255
        red = pow((red + 0.055) / (1.0 + 0.055), 2.4) if (red > 0.04045) else(red / 12.92)
        green = pow((green + 0.055) / (1.0 + 0.055), 2.4) if (green > 0.04045) else(green / 12.92)
        blue = pow((blue + 0.055) / (1.0 + 0.055), 2.4) if (blue > 0.04045) else (blue / 12.92)

        X = red * 0.664511 + green * 0.154324 + blue * 0.162028
        Y = red * 0.283881 + green * 0.668433 + blue * 0.047685
        Z = red * 0.000088 + green * 0.072310 + blue * 0.986039
        
        if(Z == 0):
            Z = .1
        x = X / (X + Y + Z)
        y = Y / (X + Y + Z)
        p = self.Point(X, Y)
        return p

    def set_light_list(self):
        g = self.b.get_group(self.group, 'lights')
        self.lights = []
        lights = self.b.get_light_objects()
        for light in g:
            self.lights.append(lights[int(light)-1])

    def get_group_status(self): 
        return self.b.get_group(self.group)

    def get_all(self):
        groups = {}
        for group in self.b.get_group():
            groups[str(self.b.get_group(int(group), 'name'))] = self.b.get_group(int(group))
        return groups


    def set_group(self, name):
        if(name.lower() == 'all'):
            self.lights = self.b.get_light_objects()
        else:
            for group in self.b.get_group():
                if(self.b.get_group(int(group), 'name') == str(name)):
                    self.group = int(group)
            self.set_light_list()

    def rgb_set(self, rgb):
        print('IN SET')
        red = float(rgb[0])
        green = float(rgb[1])
        blue = float(rgb[2])
        print('IN SET')

        point = self.convert_rgb(red, green, blue)
        print('point is',point)
        x = point[0]
        y = point[1]
        for light in self.lights:
            light.xy = [x,y]

    def brightness(self, amount):
        for light in self.lights:
            light.brightness = int(amount)

    def on(self, state):
        state = bool(state)
        for light in self.lights:
            light.on = state

    def transition(self, command):
        for light in self.lights:
            light.transitiontime = float(command['transitiontime'])
