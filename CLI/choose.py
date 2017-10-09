#!/usr/bin/python2.7
import HueController
from colour import Color
import sys
import TempToRgb
import HueController
import Weather_API

hue = HueController.hue_rgb("192.168.1.2")
hue.set_group("fan")

def get_temp():
    temp = Weather_API.Weather()
    temp.api_key = '52347449fab1dab5431fcbc264efcb19'
    temp.latitude = '40.014984'
    temp.longitude = '-105.270546'
    temp.refresh()

    rgb = TempToRgb.TempToRgb(temp.temp + 10)
    print "Weather Update: " + str(temp.temp) + " and " + str(temp.summary)
    colors = rgb.get_rgb()
    colors = list(map((lambda x:float( x/255.0 )), colors))
    return colors

if(len(sys.argv) > 2):
    hue.set_group(sys.argv[2])

if(sys.argv[1] == 'off'):
    hue.on(False)
    quit()
if(sys.argv[1] == 'on'):
    hue.on(True)
    quit()

if(sys.argv[1] == 'temp'):
    hue.rgb_set(get_temp())
    quit()


try:
    c = Color(str(sys.argv[1]))
except:
    print "Color not in dictionary"
    quit()

hue.rgb_set(c.rgb)

