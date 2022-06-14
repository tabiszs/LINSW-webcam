#!/usr/bin/python
import gpiod
import time


class Led:
    red_on = False
    green_on = False
    line = 0

    def __init__(self, type):
        self._chip = gpiod.Chip('gpiochip0')
        if type == 'stream' :
            self.line = 13
        elif type == 'photo' :
            self.line = 12
        elif type == 'internal':
            self.line = 19
        self.io = self._chip.get_line(self.line)
        self.io.request(consumer=type, type=gpiod.LINE_REQ_DIR_OUT)
        self.io.set_value(0)  

    def on(self):
        self.io.set_value(1)
    
    def off(self):
        self.io.set_value(0)