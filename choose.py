#!/usr/bin/python2.7
import HueController
from colour import Color
import sys

hue = HueController.hue_rgb("192.168.1.2")
hue.set_group("fan")

if(sys.argv[1] == 'off'):
    hue.on(False)
    quit()
if(sys.argv[1] == 'on'):
    hue.on(True)
    quit()

try:
    c = Color(str(sys.argv[1]))
except:
    print "Color not in dictionary"
    quit()

hue.rgb_set(c.rgb)
