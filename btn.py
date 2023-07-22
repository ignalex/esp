from machine import Pin
import time

class Button:
    def __init__(self, pin, callback, release_callback = None, min_ago=1000, id = None, d=None, pos=[0,30]):
        "btn with callback and release callback" 
        "debouncing stable 20ms, skip too soon second press"
        "display integration"
        self.callback = callback
        self.release_callback = release_callback
        self.min_ago = min_ago
        self.ID = id
        self.counter = 0
        self.pressed = False
        self.d = d
        self.pos = pos 
        self.ms_wait = 20
        self._next_call = time.ticks_ms() #+ self.min_ago
        pin.irq(trigger=Pin.IRQ_FALLING | Pin.IRQ_RISING, handler=self.debounce_handler)

    def call_callback(self, pin):
        self.counter += 1
        self.pressed = True
        print(f'btn {self.ID} pressed, count {self.counter}')
        if self.d is not None: 
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
            print(self.ID + ' released')
            if self.d is not None: 
                self.d.fill_rect(self.pos[0], self.pos[1], 128, 10, 0) 
                #!!!: change 128 
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
    
            
# import pins 
# b1 = Button(pin=Pin(pins.B1, mode=Pin.IN, pull=Pin.PULL_UP), callback=test, release_callback = None, min_ago = 2000, id = 'B1', None, [0,0] )

