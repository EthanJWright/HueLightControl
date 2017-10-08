#!/usr/bin/python
import random
import collections
import logging
from phue import Bridge
logging.basicConfig()

class hue_rgb():
    def __init__(self):
        self.Point = collections.namedtuple('Point', ['x', 'y'])
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

    def rgb_set(self, rgb):
        red = rgb[0]
        green = rgb[1]
        blue = rgb[2]
        b = Bridge('192.168.1.2')
# If the app is not registered and the button is not pressed, press the button
# and call connect() (this only needs to be run a single time)
        b.connect()

# Get the bridge state (This returns the full dictionary that you can explore)
        b.get_api()

        point = self.convert_rgb(red, green, blue)
#        aquamarine = convert_rgb(0.498039, 1, 0.831373,)
#        midnight_blue = convert_rgb(0.0980392, 0.0980392, 0.439216)
#        light_slate_gray = convert_rgb(0.466667, 0.533333, 0.6)
#        lavender = convert_rgb(0.901961, 0.901961, 0.980392)
#        point = lavender

        x = point[0]
        y = point[1]

        lights = b.get_light_objects()
        lights = lights[:-1]
        for light in lights:
            light.xy = [x,y]

    def on(self, state):
        b = Bridge('192.168.1.2')
        b.connect()
        b.get_api()
        lights = b.get_light_objects()
        lights = lights[:-1]
        for light in lights:
            light.on = state
#lights[0].xy = [x,y]

