#from machine import Pin
from time import sleep 

class OBJECT (object):
    "basic empty object"
    def __init__(self,d={}):
        for k,v in d.items():
            setattr(self,k,v)

def relay(pin, state=1):
    "simple relay"
    r = Pin(pin, Pin.OUT, value=state)
    return r
    
#r1 = relay(pins.R1, 1)


class RELAY: 
    "simple relay"
    def __init__(self, pin, name = 'relay', logic = 'high', debug = True): 
        self.pin = pin
        self.name = name
        self.logic = True if logic == 'high' else False
        #self.r = Pin(pin, Pin.OUT, value=state)
        self.r = OBJECT({'value':lambda x : x})
        self.state = 0 if self.logic else 1
        self.debug = debug 
        #if state: self.on() #???
    def on(self): 
        self.r.value(self.logic)
        self.state = True
        if self.debug: print(f'{self.name} set to ON')
    def off(self):
        self.r.value(not self.logic)
        self.state = False
        if self.debug: print(f'{self.name} set to OFF')


class MOTOR: 
    def __init__(self, dir, motor, name, tags = ['<', '>']):
        "dir, go - relays"
        self.dir = dir
        self.motor = motor 
        self.name = name 
        self.delay = 1
        self.tags = tags
        
    def go(self, dir = 0): 
        "go direction 0 / 1"
        if self.motor.state: 
            self.motor.off() # making sure no switch direction
            sleep(self.delay)
        if dir: 
            self.dir.on()
            sleep(self.delay)
        self.motor.on()
        print(f'{self.name} {self.tags[dir]}')
        
    def stop(self, reset_dir = False): 
        self.motor.off()
        if reset_dir: 
            self.dir.off()
        print(f'{self.name} X {"and reset" if reset_dir else ""}')
            
if __name__ == '__main__':
    r1 = RELAY(1, 'hor dir', debug = False)
    r2 = RELAY(2, 'hor drive', debug = False)
    m1 = MOTOR(r1,r2,'H')
    
    r3 = RELAY(3, 'ver dir', debug = False)
    r4 = RELAY(4, 'ver drive', debug = False)
    m2 = MOTOR(r3,r4,'V', tags = ['^', 'v'])
    
    m3 = RELAY(3, 'main')