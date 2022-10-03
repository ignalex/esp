from machine import RTC, Pin
import ntptime
from time import sleep
import time
from dust import DUST

def real_time(display=None):
    rtc = RTC()
    # synchronize with ntp
    # need to be connected to wifi
    try:
        ntptime.settime() # set the rtc datetime from the remote server
        if display is not None:
            display.text(':'.join([str(i) for i in rtc.datetime()[1:-1]]), 0, 15, 1)
            display.show()
    except:
        if display is not None:
            display.text('no real time', 0, 15, 1)
            display.show()
    return rtc

def count(display, a=1, s=1, r = None, cycle=10, stop=False, b = 1, dust=False, a_lim = 128):
    start = time.ticks_ms()
    du = ''
    for x in range(128):
        display.fill(0)
        display.text(format_seconds_to_ddhhmmss(a), 0, 0, 1)
        display.fill_rect(0, 10, a % 128, 15, 1)   # draw a solid rectangle 10,10 to 117,53, colour=1
        display.text( str((a // 128 +1) ) + ' ' +str(int((a % 128)*100/128)) + '%',  0, 14, 0)
        if r is not None: #relay
            if len(r)  > 1 :
                for k, n in enumerate (r):
                    if a % (cycle * 2) > cycle : #approx half
                        n.off()
                        display.text(str(k) + '+', k*15, 40, 1)
                        sleep(0.02)
                    else:
                        n.on()
                        display.text(str(k) + '-', k*15, 40, 1)
                        sleep(0.02)
        if a % 10 == 0 and dust:
            dust_ = DUST(50)
            du = 'dst ' + str(round(dust_['density'], 1)) + ' [' + str(int(dust_['max_'])) + ']'
        display.text(du, 0,50,1)
        display.show()
        if a % 10 == 0 and dust:
            sleep (s - 0.5)
        else:
            sleep(s)
        a += 1
        if stop and a > a_lim and r is not None:
            display.fill(0)
            print(str(b) + ' done ' + str(time.ticks_ms() - start))
            display.text(str(b) + ' done ' + str(time.ticks_ms() - start), 0, 0, 1)
            display.show()
            return

def format_seconds_to_ddhhmmss(seconds):
    days = seconds // (60*60*24)
    hours = seconds // (60*60)
    seconds %= (60*60)
    minutes = seconds // 60
    seconds %= 60
    return "%02id %02i:%02i:%02i" % (days, hours, minutes, seconds)

def relay(pin, state=0):
    r = Pin(pin, Pin.OUT, value=state)
    return r

class Button:
    def __init__(self, pin, callback, trigger= Pin.IRQ_FALLING, min_ago=500, id = None):
        # Pin.IRQ_FALLING | IRQ_RISING
        self.callback = callback
        self.min_ago = min_ago
        self.ID = id
        self.counter = 0

        self._next_call = time.ticks_ms() #+ self.min_ago
        # self._long_press = None

        pin.irq(trigger=trigger, handler=self.debounce_handler)

    def call_callback(self, pin):
        print('btn {} pressed'.format(self.ID))
        self.counter += 1
        self.callback(pin, self.ID, self.counter)

    def debounce_handler(self, pin):
        if time.ticks_ms() > self._next_call:
            self._next_call = time.ticks_ms() + self.min_ago
            self.call_callback(pin)
        else:
            print('btn {} bouncing - not processed'.format(self.ID))

    # def debounce_handler_long(self, pin):
    #     "used only for double pressing"
    #     if time.ticks_ms() > self._next_call:
    #         if self._long_press is  None:
    #             self._long_press = time.ticks_ms() + 50
    #         else:
    #             if time.ticks_ms() > self._long_press + 500: #missed
    #                 self._long_press = None
    #             elif time.ticks_ms() > self._long_press: #window between +200 -..- +400
    #                 self._next_call = time.ticks_ms() + self.min_ago
    #                 self._long_press = None
    #                 self.call_callback(pin)
    #     else:
    #         print('btn {} bouncing - not processed'.format(self.ID))

