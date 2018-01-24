import LED_controller
import time

led = LED_controller.rgb([16, 20, 21])
while(True):
    led.set([0,0,0])
    time.sleep(2)
    led.set([0,0,0])
    time.sleep(2)
    led.set([0,0,0])
    time.sleep(2)
    print('done')
led.end
