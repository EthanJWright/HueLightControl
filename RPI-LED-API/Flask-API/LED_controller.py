#!/usr/bin/env python
import pigpio

class rgb():
    def __init__(self, _gpio):
        self.rpi = pigpio.pi('192.168.1.8', 8888)
        self.gpio = _gpio

    def set(self, rgb):
         for i in range (0, 3):
             self.rpi.set_PWM_dutycycle(self.gpio[i], rgb[i])

    def end(self):
        self.rpi.stop()


