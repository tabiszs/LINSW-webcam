#!/usr/bin/python

# ustaw połączenie do przycisku pojemnościowego
# ustaw połączenie do wyjściowej diody

import os
import sys
import gpiod
import time
from camera_utils import WebCam
from led import Led

max_time=sys.maxsize #sec
bouncing_time=1 #sec
pressed=-1

class ManualPhoto:

    def __init__(self):
        self._chip = gpiod.Chip('gpiochip0')
        self.button = self._chip.get_line(12) #was 10
        self._cam = WebCam()
        self._led = Led('internal')
        
    def handle_input_button(self):
        self.button.request(consumer="button", type=gpiod.LINE_REQ_EV_BOTH_EDGES)       
        while True:                        
            print('waiting for press')                         
            ev_line = self.button.event_wait(sec=max_time)
                            
            if ev_line:       
                print('read event')             
                event = self.button.event_read()
                if (event.type == gpiod.LineEvent.RISING_EDGE) & (pressed):                    
                    self.save_photo()
                self.process_event(event)      
            else:                        
                print('waiting time end')
                break

    def save_photo(self):
        print('Save Photo')
        self._led.on()
        self._cam.open()
        self._cam.save_image()
        path2 = os.path.dirname(os.path.realpath(__file__)) + '/image'  
        filename = self._cam.save_image(path2)
        print(filename)
        self._cam.release()
        self._led.off()

    def process_event(self, event):
        print('process event')
        while True:
            if event.type == gpiod.LineEvent.RISING_EDGE:
                evstr = 'RISING EDGE'
                self.pressed = 0
            elif event.type == gpiod.LineEvent.FALLING_EDGE:
                evstr = 'FALLING EDGE'
                self.pressed = 1
            else:
               raise TypeError('Invalid event type')

            print('event: {} offset: {} timestamp: [{}.{}]'.format(evstr,event.source.offset(),event.sec, event.nsec))
        
            ev_line = self.button.event_wait(bouncing_time)
            
            if ev_line:
                event = self.button.event_read()
                print('bouncing event: {} offset: {} timestamp: [{}.{}]'.format(evstr,event.source.offset(),event.sec, event.nsec))
            else:
                print('bouncing timeout')
                break

if __name__ == '__main__':
    mp=ManualPhoto()
    mp.handle_input_button()
