#!/usr/bin/env python
import pigpio
import ConfigParser

class rgb():
    def __init__(self, _gpio):
        self.config = ConfigParser.ConfigParser()
        config.read('iot.properties')
        self.rpi = pigpio.pi(config.get('RPI LED'), 8888)
        self.gpio = _gpio

    def set(self, rgb):
         for i in range (0, 3):
             self.rpi.set_PWM_dutycycle(self.gpio[i], rgb[i])

    def end(self):
        self.rpi.stop()


