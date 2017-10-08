import TempToRgb
import HueController
import Weather_API


temp = Weather_API.Weather()
temp.api_key = '52347449fab1dab5431fcbc264efcb19'
temp.latitude = '40.014984'
temp.longitude = '-105.270546'

temp.refresh()

rgb = TempToRgb.TempToRgb(temp.temp + 10)
colors = rgb.get_rgb()
colors = list(map((lambda x:float( x/255.0 )), colors))
hue = HueController.hue_rgb("192.168.1.2")
hue.set_group("fan")
hue.rgb_set(colors)
