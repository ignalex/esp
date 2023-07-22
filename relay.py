MOTOR_DELAY = 1


try:
    from machine import Pin
except: 
    print('no machine module available >> testing only')
    
from time import sleep 

class OBJECT (object):
    "basic empty object"
    def __init__(self,d={}):
        for k,v in d.items():
            setattr(self,k,v)

# simple 
def relay(pin, state=1):
    "simple relay"
    r = Pin(pin, Pin.OUT, value=state)
    return r
    
#r1 = relay(pins.R1, 1)


class RELAY: 
    "relay"
    def __init__(self, pin, name = 'relay', logic = 'high', wait = {'on': 0, 'off': 0}, \
            d = None, pos = [10, 0], tags = ['  ', 'R+'], \
            debug = True): 
        self.pin = pin
        self.name = name
        self.wait = wait # wait for cooling down 
        self.logic = True if logic == 'high' else False
        try: 
            self.r = Pin(pin, Pin.OUT, value=state)
        except: 
            self.r = OBJECT({'value':lambda x : x})
            print(f'relay {self.name} testing only')
        self.state = 0 if self.logic else 1
        self.debug = debug 
        #if state: self.on() #???
        self.d = d 
        self.pos = pos 
        self.tags = tags 
        
    def on(self): 
        self.r.value(self.logic)
        self.state = True
        if self.debug: print(f'{self.name} set to ON')
        self.display(1)
        self.sleep(self.wait['on'])
        
    def off(self):
        self.r.value(not self.logic)
        self.state = False
        if self.debug: print(f'{self.name} set to OFF')
        self.display(0)
        self.sleep(self.wait['off'])
        
    def sleep(self, x): 
        if x != 0: 
            if self.debug: print(f'waiting {x}', end='')
            sleep(x)
            if self.debug: print(' DONE')
    
    def display(self, id): 
        if self.d is not None: 
            self.fill()
            self.d.fill_rect(self.pos[0], self.pos[1], len(self.tags[id]) * 10, 10, 0) 
            self.d.text(self.tags[id], self.pos[0], self.tags[1], 1)
            self.d.show()

class MOTOR: 
    def __init__(self, dir, motor, name, tags = ['<', '>'], d = None, pos = [0,30]):
        "dir, motor - relays"
        self.dir = dir
        self.motor = motor 
        self.name = name 
        self.delay = MOTOR_DELAY
        self.tags = tags
        self.d = d # display and text position 
        self.pos = pos
        
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
        if self.d is not None: 
            self.d.text(f'{self.tags[dir]}', self.pos[0], self.pos[1], 1)
            self.d.show()
            
    def stop(self, reset_dir = False): 
        self.motor.off()
        if reset_dir: 
            self.dir.off()
        print(f'{self.name} X {"and reset" if reset_dir else ""}')
        if self.d is not None: 
            self.d.fill_rect(self.pos[0], self.pos[1], 10, 10, 0) # what is 1 symb width? 
            self.d.show()
            
if __name__ == '__main__':
    r1 = RELAY(1, 'HORIZONTAL dir', debug = True)
    r2 = RELAY(2, 'HORIZONTAL drive', debug = True)
    m1 = MOTOR(r1,r2,'H', tags = ['<', '>'])
    
    r3 = RELAY(3, 'VERTICAL dir', debug = False)
    r4 = RELAY(4, 'VERTICAL drive', debug = False)
    m2 = MOTOR(r3,r4,'V', tags = ['^', 'v'])
    
    m3 = RELAY(3, 'main', wait = dict(on=1,off=1))