# -*- coding: utf-8 -*-

#TODO: full time mode. > ignore btns, use timings. 
#TODO: mode btn on start not to return00 
#TODO: move as array? ['left', 'up']
#TODO: all statuses > else (loading etc)

# workflow 
# loading > initializing > ready > working > finishing. stop, cancelling
# move: left right down / up

import time
import pins 
import config

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
        
        
    Pin = OBJECT(dict(id=1, mode = '', pull = '', value = '', IN = 1, \
                      PULL_UP = 1, IRQ_FALLING = '', IRQ_RISING = '', ))
    time.ticks_ms = lambda  : 0
    

class PILLY:
    def __init__(self, d=None): 
        "b, r - reserverd for [b1,...], [r1,..,m1...]"
        "btns, relays > add when methods available (callbacks)"
        
        self.d = d # display 
        self.position = [None,None] #unknown
        self.status = 'loading'
        self.move = None # 
        
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
            self.d.fill_rect(self.pos[0], self.pos[1], len(text) * 8, 10, 0) 
            self.d.text(text, self.pos[0], self.pos[1], 1)
            self.d.show()
        print(text)
            
    def initialize(self):
        print('initializing')
        self.status = 'initializing'
        for k, r in self.r.__dict__.items(): 
            r.off()
            
        if self.position == [None, None]: 
            if config.ON_START_RETURN00:
                self.return00()
            else: 
                # start from whatever position
                self.ready()
    
    def return00(self): 
        "return to 00 from unknown"
        print('returning 0 0')
        self.move = 'return 00'
        self.r.V.go(0)
        # if locaiton is very down and M is off > can't start horizontal move
        time.sleep(config.TIME_HORIZONTAL_DELAY_ON_RETURN)
        self.r.H.go(0)

    def test(self, x, status=0):
        print('test ' + str(x) + ' ' + str(status))
        
    def left(self,x, status=0): 
        print('left pressed')
        self.r.H.stop()
        self.position[0] = 0
        
        if self.status in ('initializing', 'finishing') and self.b.LEFT.pressed and self.b.TOP.pressed: 
            self.ready()
        
        if self.status == 'working' and self.move == 'left':
            # normal cycle, left position
            if not self.b.BOTTOM.pressed: #!!!: what if status changed in between ? 
                self.r.V.go(1) #go down
                self.move = 'down'
                time.sleep(config.TIME_GO_DOWN_LEFT)
                if self.status == 'working' and not self.b.BOTTOM.pressed: 
                    self.r.V.stop()
                time.sleep(config.TIME_WAIT_BETWEEN_STEPS)
                if self.status == 'working' and not self.b.BOTTOM.pressed:
                    self.move = 'right'
                    self.r.H.go(1) # start go left
            else: 
                # right and bottom > finish
                self.finish()
        
    def left_released(self,x, status=0): 
        print('left released')
        self.position[0] = 1
        
    def right(self,x, status=0):
        print('right pressed')
        self.r.H.stop()
        self.position[0] = 100
        
        if self.status == 'working' and self.move == 'right':
            # normal cycle, right position
            if not self.b.BOTTOM.pressed: #!!!: what if status changed in between ? 
                self.r.V.go(1) #go down
                self.move = 'down'
                time.sleep(config.TIME_GO_DOWN_RIGHT)
                if self.status == 'working' and not self.b.BOTTOM.pressed: 
                    self.r.V.stop()
                time.sleep(config.TIME_WAIT_BETWEEN_STEPS)
                if self.status == 'working' and not self.b.BOTTOM.pressed:
                    self.move = 'left'
                    self.r.H.go(0) # start go left
            else: 
                # right and bottom > finish
                self.finish()

    def right_released(self,x, status=0): 
        print('right released')
        self.position[0] = 99
                
    def top(self,x, status=0):
        print('top pressed') 
        self.r.V.stop()
        self.position[1] = 0
        
        if self.status in ('initializing', 'finishing') and self.b.LEFT.pressed and self.b.TOP.pressed: 
            self.ready()

    def top_released(self,x, status=0): 
        print('top released')
        self.position[1] = 1
        
    def bottom(self,x, status=0): 
        print('bottom pressed')
        self.r.V.stop()
        self.position[1] = 100
        
        if self.status == 'working' and self.move == 'down':
            self.finish()

    def bottom_released(self,x, status=0): 
        print('bottom released')   
        self.position[1] = 99
        
    def red(self,x, status=0): 
        print('red pressed')
        
        # if working > stop H V M 
        if self.status == 'working': 
            self.status = 'stop'
            self.previous_move = self.move #preserving direction
            self.move = None
            self.r.M.off()
            self.r.V.off()
            self.r.H.off()
            self.display('stop', [0,0])
            
        # if red after black (when stopped) > return to 00
        elif self.status == 'stop': 
            self.display('cancelling', [0,0])
            self.status = 'cancelling'
            time.sleep(config.TIME_CANCELLING)
            if self.status == 'cancelling': 
                # nothing changed > go home
                self.return00()
        elif self.status == 'cancelling': 
            self.status = 'stop'
            self.display('stop', [0,0])

    def red_released(self,x, status=0): 
        print('red released')   
                          
    def black(self,x, status=0): 
        print('black pressed')
        
        # when ready > start 
        if self.status == 'ready': 
            self.status = 'working'
            if not self.r.M.state: 
                self.r.M.on()
            time.sleep(config.TIME_WAIT_MAIN)
            self.move = 'right'
            self.r.H.go(1)
            self.display('working', [0,0])
            
        # when working > stop H V but not M and wait 
        elif self.status == 'working': 
            self.status = 'stop'
            self.previous_move = self.move #preserving direction
            self.move = None
            #self.r.M.off()
            self.r.V.off()
            self.r.H.off()
            self.display('stop', [0,0])
            
        # second press when stopped - resume same direction
        elif self.status in ('stop', 'cancelling'): 
            self.status = 'working'
            self.r.M.on()
            if self.previous_move == 'right': 
                self.r.H.go(1)
                self.move = 'right'
                self.display('working', [0,0])
            elif self.previous_move == 'left': 
                self.r.H.go(0)
                self.move = 'left'
                self.display('working', [0,0])
            elif self.previous_move == 'down': 
                # do not go more down 
                if self.position[0] <= 1: 
                    self.r.H.go(1)
                    self.move = 'right'
                    self.display('working', [0,0])
                elif self.position[0] >= 99: 
                    self.r.H.go(0)
                    self.move = 'left'
                    self.display('working', [0,0])
            elif self.previous_move == 'return 00': 
                self.return00()
            

    def black_released(self,x, status=0): 
        print('black released')   
    
    def ready(self): 
        self.display('ready', [0, 0])
        time.sleep(config.TIME_READY)
        self.status = 'ready'
    
    def finish(self): 
        self.status = 'finishing'
        self.display('finishing', [0, 0])
        self.r.M.off()
        time.sleep(config.TIME_FINISH)
        self.return00()
                                              
    
if __name__ == '__main__': 
    from relay import RELAY, MOTOR
    from btn import Button
    
    r1 = RELAY(pins.R1, 'HORIZONTAL dir', debug = config.DEBUG, \
               wait = dict(on=config.TIME_WAIT_HDIR_ON, off=config.TIME_WAIT_HDIR_OFF))
    r2 = RELAY(pins.R2, 'HORIZONTAL drive', debug = config.DEBUG, \
               wait = dict(on=config.TIME_WAIT_HGO_ON, off=config.TIME_WAIT_HGO_OFF))
    m1 = MOTOR(r1,r2,'H', tags = ['<', '>'], d = None, pos = [0,3])
    
    r3 = RELAY(pins.R3, 'VERTICAL dir', debug = config.DEBUG, \
               wait = dict(on=config.TIME_WAIT_VDIR_ON, off=config.TIME_WAIT_VDIR_OFF))
    r4 = RELAY(pins.R4, 'VERTICAL drive', debug = config.DEBUG, \
               wait = dict(on=config.TIME_WAIT_VGO_ON, off=config.TIME_WAIT_VGO_OFF))
    m2 = MOTOR(r3,r4,'V', tags = ['^', 'v'], d = None, pos = [5,3])
    
    m3 = RELAY(pins.R5, 'M', \
               wait = dict(on=config.TIME_WAIT_MAIN_ON, off=config.TIME_WAIT_MAIN_OFF), \
               d = None, pos = [10, 3])
    
    p = PILLY()
    
    b1 = Button(pin=Pin(pins.B1, mode=Pin.IN, pull=Pin.PULL_UP), \
                callback=p.left, release_callback = p.left_released, \
                min_ago = config.WAIT_BETWEEN_PRESSED_MS, \
                id = 'LEFT', d = None, pos = [0,1] )

    b2 = Button(pin=Pin(pins.B2, mode=Pin.IN, pull=Pin.PULL_UP), \
                callback=p.right, release_callback = p.right_released, \
                min_ago = config.WAIT_BETWEEN_PRESSED_MS, \
                id = 'RIGTH', d = None, pos = [2,1] )

    b3 = Button(pin=Pin(pins.B3, mode=Pin.IN, pull=Pin.PULL_UP), \
                callback=p.top, release_callback = p.top_released, \
                min_ago = config.WAIT_BETWEEN_PRESSED_MS, \
                id = 'TOP', d = None, pos = [4,1] )

    b4 = Button(pin=Pin(pins.B4, mode=Pin.IN, pull=Pin.PULL_UP), \
                callback=p.bottom, release_callback = p.bottom_released, \
                min_ago = config.WAIT_BETWEEN_PRESSED_MS, 
                id = 'BOTTOM', d = None, pos = [6,1] )

    red = Button(pin=Pin(pins.B5, mode=Pin.IN, pull=Pin.PULL_UP), \
                callback=p.red, release_callback = p.red_released, \
                min_ago = config.WAIT_BETWEEN_PRESSED_MS, \
                id = 'RED', d = None, pos = [8,1] )

    black = Button(pin=Pin(pins.B6, mode=Pin.IN, pull=Pin.PULL_UP), \
                callback=p.black, release_callback = p.black_released, \
                min_ago = config.WAIT_BETWEEN_PRESSED_MS, \
                id = 'BLACK', d = None, pos = [10,1] )

    p.hook_pereferials(btns=[b1, b2, b3, b4, red, black], \
                       relays=[m1,m2,m3])
             
    p.initialize()








