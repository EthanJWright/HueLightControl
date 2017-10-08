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

    def set_group(self, name):
        for group in self.b.get_group():
            if(self.b.get_group(int(group), 'name') == name):
                self.group = int(group)
        self.set_light_list()

    def rgb_set(self, rgb):
        red = rgb[0]
        green = rgb[1]
        blue = rgb[2]

        point = self.convert_rgb(red, green, blue)
        x = point[0]
        y = point[1]
        for light in self.lights:
            light.xy = [x,y]

    def on(self, state):
        for light in self.lights:
            light.on = state

