#!/usr/bin/python2.7
import Hue_controller
from colour import Color
import sys

if(sys.argv[1] == 'off'):
    hue = Hue_controller.hue_rgb()
    hue.on(False)
    quit()
if(sys.argv[1] == 'on'):
    hue = Hue_controller.hue_rgb()
    hue.on(True)
    quit()

try:
    c = Color(str(sys.argv[1]))
except:
    print "Color not in dictionary"
    quit()

hue = Hue_controller.hue_rgb()
hue.rgb_set(c.rgb)
