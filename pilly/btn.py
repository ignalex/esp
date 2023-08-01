import time
import pins
import config 

from log import LOG

# for testing on non-esp 
try: 
    from machine import Pin
except: 
    print('no machine module > testing only')
    class OBJECT (object):
        "basic empty object"
        def __init__(self,d={}):
            for k,v in d.items():
                setattr(self,k,v)
        def __call__(self, *args, **kargs): 
            pass 
        
        def irq(self,trigger, handler): 
            pass 
        
    Pin = OBJECT(dict(id=1, mode = '', pull = '', value = '', IN = 1, PULL_UP = 1, \
    IRQ_FALLING = '', IRQ_RISING = '', ))
    time.ticks_ms = lambda  : 0


class Button:
    def __init__(self, pin, callback, release_callback = None, min_ago=1000, id = None, name = 'BTN', d=None, pos=[0,30], debug=False, log=print):
        "btn with callback and release callback" 
        "debouncing stable 20ms, skip too soon second press"
        "display integration"
        self.callback = callback
        self.release_callback = release_callback
        self.min_ago = min_ago
        self.ID = id
        self.name = name
        self.counter = 0
        self.pressed = False
        self.d = d
        self.pos = pos 
        self.ms_wait = config.DEBOUNCE_MS
        self._next_call = time.ticks_ms() #+ self.min_ago
        self.print = log
        self.debug = debug
        try: 
            pin.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=self.debounce_handler)
        except: 
            self.print(f'{self.name} no irq registered > testing only')
            
    def call_callback(self, pin):
        self.counter += 1
        self.pressed = True
        if self.debug: self.print(f'btn {self.ID} pressed, count {self.counter}')
        if self.d is not None: 
            self.d.fill_rect(self.pos[0], self.pos[1], 8 * len(self.ID), 10, 0)
            self.d.text(self.ID, self.pos[0], self.pos[1], 1)
            self.d.show()
        self.callback(self.ID, self.pressed)

    def debounce_handler(self, pin):
        if time.ticks_ms() > self._next_call: 
            self._next_call = time.ticks_ms() + self.min_ago
            s = self.wait_pin_change(pin)
            if s and not self.pressed: 
                self.call_callback(pin)
            elif s and self.pressed: 
                pass 
            elif not s and not self.pressed: 
                pass 
            else: 
                self.release_handler(pin)
        else:
            s = self.wait_pin_change(pin)
            if not s and  self.pressed: 
                self.release_handler(pin)

    def release_handler(self, pin):
        if self.pressed: 
            self.pressed = False
            if self.debug: self.print(self.ID + ' released')
            if self.d is not None: 
                self.d.fill_rect(self.pos[0], self.pos[1], 8 * 10, 10, 0) #!!!: check 
                self.d.show()
            if self.release_callback is not None: 
                self.release_callback(self.ID, self.pressed)
            
    def wait_pin_change(self, pin):
        # wait for pin to change value
        # it needs to be stable for a continuous 20ms
        cur_value = pin.value()
        active = 0
        while active < self.ms_wait:
            if pin.value() == cur_value:
                active += 1
            else:
                active = 0
                cur_value = pin.value()
            time.sleep_ms(1)
        return not pin.value()


def test(x, status=0):
    print('test ' + str(x) + ' ' + str(status))
    
  
if __name__ == '__main__': 
    log = LOG(True)
    b1 = Button(pin=Pin(pins.B1, mode=Pin.IN, pull=Pin.PULL_UP), callback=test, release_callback = None, min_ago = config.WAIT_BETWEEN_PRESSED_MS, id = 'B1', name = 'LEFT', d = None, pos = [0,0], log=log, debug=True)




