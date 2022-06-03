#!/usr/bin/python
import gpiod
import time


class Led:
    red_on = False
    green_on = False

    def __init__(self):
        self._chip = gpiod.Chip('gpiochip0')
        self._red = self._chip.get_line(13)
        self._green = self._chip.get_line(12)
        self._red.request(consumer="webcam", type=gpiod.LINE_REQ_DIR_OUT)
        self._green.request(consumer="webcam", type=gpiod.LINE_REQ_DIR_OUT)

    def on(self, type):
        if type == 'red':
            self._red.set_value(1)
        if type == 'green':
            self._green.set_value(1)
    
    def off(self, type):
        if type == 'red':
            self._red.set_value(0)
        if type == 'green':
            self._green.set_value(0)

