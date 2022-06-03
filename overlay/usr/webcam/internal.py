#!/usr/bin/python

# ustaw połączenie do przycisku pojemnościowego
# ustaw połączenie do wyjściowej diody

import gpiod
import time

chip = gpiod.Chip('gpiochip0')
button = chip.get_line(10)
max_time=3600 #sec
bouncing_time=300 #msec
pressed=-1


def handle_input_button():
    while True:
        # oczekuj na nacisniecie/zwlolnienie
        button.request(consumer="button", type=gpiod.LINE_REQ_EV_BOTH_EDGES)
        ev_line = button.event_wait(sec=max_time)
        if ev_line:    
            # oczytaj zdarzenie
            event = button.event_read()
            # przetwarzaj zdarzenie            
            print_event(event)
            if event == gpiod.LineEvent.FALLING_EDGE:
                # przycisk jest zwalniany, zrób zdjęcie
                m=2
        else:
            # upłynął czas oczekiwania 
            break 
        

def print_event(event):
    while True:
        if event.type == gpiod.LineEvent.RISING_EDGE:
            evstr = 'RISING EDGE'
            pressed = 1
        elif event.type == gpiod.LineEvent.FALLING_EDGE:
            evstr = 'FALLING EDGE'
            pressed = 0
        else:
            raise TypeError('Invalid event type')

        print('event: {} offset: {} timestamp: [{}.{}]'.format(evstr,event.source.offset(),event.sec, event.nsec))
        button.request(consumer="button", type=gpiod.LINE_REQ_EV_BOTH_EDGES)
        ev_line = button.event_wait(sec=bouncing_time)
        if ev_line < 0:
            break # upłynął czas bauncingu

if __name__ == '__main__':
    handle_input_button()
