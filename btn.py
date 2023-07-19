from machine import Pin
import time

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
            
def test(x):
    print('test ' + str(x))
    
    
# import pins 
# b1 = Button(pin=Pin(pins.B1, mode=Pin.IN, pull=Pin.PULL_UP), callback=test, min_ago = 2000, id = 'B1' )