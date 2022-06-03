#!/usr/bin/python

# ustaw połączenie do przycisku pojemnościowego
# ustaw połączenie do wyjściowej diody

import os
import gpiod
import time

from camera_utils import WebCam
from led import Led

max_time=3600 #sec
#max_time=sys.maxsize
bouncing_time=300 #msec
pressed=-1

class ManualPhoto:

    def __init__(self):
        self._chip = gpiod.Chip('gpiochip0')
        self.button = self._chip.get_line(10)
        self._cam = WebCam()
        self._led = Led('photo')
        

    def handle_input_button(self):
        while True:
            # oczekuj na nacisniecie/zwlolnienie
            self.button.request(consumer="button", type=gpiod.LINE_REQ_EV_BOTH_EDGES)
            self.ev_line = self.button.event_wait(sec=max_time)

            if self.ev_line:    
                # oczytaj zdarzenie
                event = self.button.event_read()
                self.button.release()
                self.button = self._chip.get_line(10)
                # przetwarzaj zdarzenie            
                self.print_event(event)
                if event == gpiod.LineEvent.FALLING_EDGE:
                   # przycisk jest zwalniany, zrób zdjęcie
                    self._led.on()
                    self._cam.open()
                    self._cam.save_image()
                    path2 = os.path.dirname(os.path.realpath(__file__)) + '/image'  
                    filename = self._cam.save_image(path2)
                    print(filename)
                    self._cam.release()
                    self._led.off()
            else:
                # upłynął czas oczekiwania
                self.button.release()
                self.button = self._chip.get_line(10)
                break 
        

    def print_event(self, event):
        while True:
            if event.type == gpiod.LineEvent.RISING_EDGE:
                evstr = 'RISING EDGE'
                self.pressed = 1
            elif event.type == gpiod.LineEvent.FALLING_EDGE:
                evstr = 'FALLING EDGE'
                self.pressed = 0
            else:
                raise TypeError('Invalid event type')

            print('event: {} offset: {} timestamp: [{}.{}]'.format(evstr,event.source.offset(),event.sec, event.nsec))
            self.button.request(consumer="button", type=gpiod.LINE_REQ_EV_BOTH_EDGES)
            ev_line = self.button.event_wait(sec=bouncing_time)
            self.button.release()
            self.button = self._chip.get_line(10)
            if ev_line < 0:
                break # upłynął czas bauncingu

if __name__ == '__main__':
    mp=ManualPhoto()
    mp.handle_input_button()
