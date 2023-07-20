from machine import Pin
import time

class Button:
    def __init__(self, pin, callback, trigger= Pin.IRQ_FALLING, min_ago=500, id = None):
        # Pin.IRQ_FALLING | IRQ_RISING
        self.callback = callback
        self.min_ago = min_ago
        self.ID = id
        self.counter = 0
        self.pressed = False

        self._next_call = time.ticks_ms() #+ self.min_ago

        pin.irq(trigger=trigger, handler=self.debounce_handler)

    def call_callback(self, pin):
        print('btn {} pressed'.format(self.ID))
        self.counter += 1
        self.callback(pin)

    def debounce_handler(self, pin):
        if time.ticks_ms() > self._next_call:
            self._next_call = time.ticks_ms() + self.min_ago
            self.call_callback(pin)
        else:
            print('btn {} bouncing - not processed'.format(self.ID))
            
class Button2:
    def __init__(self, pin, callback, min_ago=500, id = None):
        # Pin.IRQ_FALLING | IRQ_RISING
        self.callback = callback
        self.min_ago = min_ago
        self.ID = id
        self.counter = 0
        self.pressed = False

        self._next_call = time.ticks_ms() #+ self.min_ago

        pin.irq(trigger=Pin.IRQ_FALLING, handler=self.debounce_handler)
        pin.irq(trigger=Pin.IRQ_RISING,  handler=self.release_handler)

    def call_callback(self, pin):
        print('btn {} pressed'.format(self.ID))
        self.counter += 1
        self.pressed = True
        self.callback(pin)

    def debounce_handler(self, pin):
        if time.ticks_ms() > self._next_call and not self.pressed:
            self._next_call = time.ticks_ms() + self.min_ago
            self.call_callback(pin)
        else:
            print('btn {} bouncing - not processed'.format(self.ID))            
            
    def release_handler(self, pin):
        if self.pressed: 
            self.pressed = False
            print(self.ID + ' released')



def test(x):
    print('test ' + str(x))
    
    
# import pins 
# b1 = Button(pin=Pin(pins.B1, mode=Pin.IN, pull=Pin.PULL_UP), callback=test, min_ago = 2000, id = 'B1' )