# -*- coding: utf-8 -*-

#TODO: init class first, add relays, add btns (pass callbacks)

import time
import pins 

class Object(object):
    pass

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
    

class PILLY:
    def __init__(self, d=None): 
        "b, r - reserverd for [b1,...], [r1,..,m1...]"
        "btns, relays > add when methods available (callbacks)"
        
        self.d = d # display 
        self.position = [None,None] #unknown
        self.status = 'loading'
        
    def hook_pereferials(self, btns=[], relays=[]): 
        print()
        print("adding btns")
        
        self.b = Object()
        for b in btns: 
            setattr(self.b, b.name, b)
            #self.b.append(b) 
        
        print("adding relays")
        self.r = Object()
        for r in relays: 
            setattr(self.r ,r.name, r)
            
    def display(self, text, pos): 
        if self.d is not None: 
            self.d.fill_rect(self.pos[0], self.pos[1], len(text) * 10, 10, 0) 
            self.d.text(text, self.pos[0], self.pos[1], 1)
            self.d.show()
        print(text)
            
    def initialize(self):
        print('initializing')
        self.status = 'initializing'
        for k, r in self.r.__dict__.items(): 
            r.off()
            
        if self.position == [None, None]:
            self.return00()
            
        self.display('initialized', [0, 0])
        self.status = 'ready'
    
    def return00(self): 
        "return to 00 from unknown"    
        self.position = [0,0]

    def test(self, x, status=0):
        print('test ' + str(x) + ' ' + str(status))
        
    def left(self,x, status=0): 
        print('left pressed')

    def left_released(self,x, status=0): 
        print('left released')
        
    def right(self,x, status=0): 
        print('right pressed')

    def right_released(self,x, status=0): 
        print('right released')
        
    def top(self,x, status=0): 
        print('top pressed')

    def top_released(self,x, status=0): 
        print('top released')
        
    def bottom(self,x, status=0): 
        print('bottom pressed')

    def bottom_released(self,x, status=0): 
        print('bottom released')   
        
    def red(self,x, status=0): 
        print('red pressed')

    def red_released(self,x, status=0): 
        print('red released')   
                          
    def black(self,x, status=0): 
        print('black pressed')

    def black_released(self,x, status=0): 
        print('black released')   
                                              
    
if __name__ == '__main__': 
    from relay import RELAY, MOTOR
    from btn import Button
    
    r1 = RELAY(1, 'HORIZONTAL dir', debug = True)
    r2 = RELAY(2, 'HORIZONTAL drive', debug = True)
    m1 = MOTOR(r1,r2,'H', tags = ['<', '>'])
    
    r3 = RELAY(3, 'VERTICAL dir', debug = False)
    r4 = RELAY(4, 'VERTICAL drive', debug = False)
    m2 = MOTOR(r3,r4,'V', tags = ['^', 'v'])
    
    m3 = RELAY(3, 'M', wait = dict(on=1,off=1))
    
    p = PILLY()
    
    b1 = Button(pin=Pin(pins.B1, mode=Pin.IN, pull=Pin.PULL_UP), \
                callback=p.left, release_callback = p.left_released, min_ago = 2000, \
                id = 'LEFT', d = None, pos = [0,0] )

    b2 = Button(pin=Pin(pins.B2, mode=Pin.IN, pull=Pin.PULL_UP), \
                callback=p.right, release_callback = p.right_released, min_ago = 2000, \
                id = 'RIGTH', d = None, pos = [0,0] )

    b3 = Button(pin=Pin(pins.B3, mode=Pin.IN, pull=Pin.PULL_UP), \
                callback=p.top, release_callback = p.top_released, min_ago = 2000, \
                id = 'TOP', d = None, pos = [0,0] )

    b4 = Button(pin=Pin(pins.B4, mode=Pin.IN, pull=Pin.PULL_UP), \
                callback=p.bottom, release_callback = p.bottom_released, min_ago = 2000, 
                id = 'BOTTOM', d = None, pos = [0,0] )

    red = Button(pin=Pin(pins.B5, mode=Pin.IN, pull=Pin.PULL_UP), \
                callback=p.red, release_callback = p.red_released, min_ago = 2000, \
                id = 'RED', d = None, pos = [0,0] )

    black = Button(pin=Pin(pins.B6, mode=Pin.IN, pull=Pin.PULL_UP), \
                callback=p.black, release_callback = p.black_released, min_ago = 2000, \
                id = 'BLACK', d = None, pos = [0,0] )

    p.hook_pereferials(btns=[b1, b2, b3, b4, red, black], \
                       relays=[m1,m2,m3])
             
    p.initialize()








