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
    def __init__(self, d=None, log=print): 
        "b, r - reserverd for [b1,...], [r1,..,m1...]"
        "btns, relays > add when methods available (callbacks)"
        
        self.d = d # display 
        self.position = [None,None] #unknown
        self.status = 'loading'
        self.move = None # 
        self.print = log
        
    def hook_pereferials(self, btns=[], relays=[]): 
        self.print()
        self.print("adding btns")
        
        self.b = Object()
        for b in btns: 
            setattr(self.b, b.name, b)
            #self.b.append(b) 
        
        self.print("adding relays")
        self.r = Object()
        for r in relays: 
            setattr(self.r ,r.name, r)
            
    def display(self, text, pos): 
        if self.d is not None: 
            self.d.fill_rect(pos[0], pos[1], len(text) * 8, 10, 0) 
            self.d.text(text, pos[0], pos[1], 1)
            self.d.show()
        self.print(text)
            
    def initialize(self):
        self.print('initializing')
        self.status = 'initializing'
        for k, r in self.r.__dict__.items(): 
            r.off()
            
        if self.position == [None, None]: 
            if config.ON_START_RETURN00:
                self.return_top()
            else: 
                # start from whatever position
                self.ready()
    
    def return_top(self): 
        "return to 00 from unknown"
        self.print('returning 0 0')
        self.move = 'return 00'
        self.r.DOWN.off(); self.r.UP.on() #self.r.V.go(0)
        # if locaiton is very down and M is off > can't start horizontal move
        #time.sleep(config.TIME_HORIZONTAL_DELAY_ON_RETURN)
        #self.r.RIGHT.off(); self.r.LEFT.on() #self.r.H.go(0)

    def test(self, x, status=0):
        self.print('test ' + str(x) + ' ' + str(status))
        
    def left(self,x, status=0): 
        self.print('left pressed')
        self.r.LEFT.off() #self.r.H.stop()
        self.position[0] = 0
        
        #if self.status in ('initializing', 'finishing') and self.b.LEFT.pressed and self.b.TOP.pressed: self.ready()
        
        if self.status == 'working' and self.move == 'left': 
            # normal cycle, left position
            if not self.b.BOTTOM.pressed: #!!!: what if status changed in between ? 
                self.r.UP.off(); self.r.DOWN.on() #self.r.V.go(1) #go down
                self.move = 'down'
                time.sleep(config.TIME_GO_DOWN_LEFT)
                if self.status == 'working' and not self.b.BOTTOM.pressed: 
                    self.r.DOWN.off() #self.r.V.stop()
                time.sleep(config.TIME_WAIT_BETWEEN_STEPS)
                if self.status == 'working' and not self.b.BOTTOM.pressed:
                    self.move = 'right'
                    self.r.LEFT.off(); self.r.RIGHT.on() #self.r.H.go(1) # start go right
            else: 
                # right and bottom > finish
                self.finish()
        
    def left_released(self,x, status=0): 
        self.print('left released')
        self.position[0] = 1
        
    def right(self,x, status=0):
        self.print('right pressed')
        self.r.RIGHT.off() #self.r.H.stop()
        self.position[0] = 100
        
        if self.status == 'working' and self.move == 'right': 
            # normal cycle, right position
            if not self.b.BOTTOM.pressed: #!!!: what if status changed in between ? 
                self.r.UP.off(); self.r.DOWN.on() #self.r.V.go(1) #go down
                self.move = 'down'
                time.sleep(config.TIME_GO_DOWN_RIGHT)
                if self.status == 'working' and not self.b.BOTTOM.pressed: 
                    self.r.DOWN.off(); self.r.UP.off() #self.r.V.stop()
                time.sleep(config.TIME_WAIT_BETWEEN_STEPS)
                if self.status == 'working' and not self.b.BOTTOM.pressed:
                    self.move = 'left'
                    self.r.RIGHT.off(); self.r.LEFT.on() #self.r.H.go(0) # start go left
            else: 
                # right and bottom > finish
                self.finish()

    def right_released(self,x, status=0): 
        self.print('right released')
        self.position[0] = 99
                
    def top(self,x, status=0):
        self.print('top pressed') 
        self.r.UP.off() #self.r.V.stop()
        self.position[1] = 0
        
        if self.status in ('initializing', 'finishing'): 
            self.ready()

    def top_released(self,x, status=0): 
        self.print('top released')
        self.position[1] = 1
        
    def bottom(self,x, status=0): 
        self.print('bottom pressed')
        self.r.DOWN.off() #self.r.V.stop()
        self.position[1] = 100
        
        if self.status == 'working' and self.move == 'down':
            self.finish()

    def bottom_released(self,x, status=0): 
        self.print('bottom released')   
        self.position[1] = 99
        
    def red(self,x, status=0): 
        self.print('red pressed')
        
         #if working > stop H V M 
        if self.status == 'working': 
            self.status = 'stop'
            self.previous_move = self.move #preserving direction
            self.move = None
            self.r.MAIN.off()
            self.r.RIGHT.off()
            self.r.LEFT.off()
            self.r.UP.off()
            self.r.DOWN.off()
            self.display('stop', [0,0])
            
         #if red after black (when stopped) > return to 00
        elif self.status == 'stop': 
            self.display('cancelling', [0,0])
            self.status = 'cancelling'
            time.sleep(config.TIME_CANCELLING)
            if self.status == 'cancelling': 
#                 nothing changed > go home
                self.return_top()
        elif self.status == 'cancelling': 
            self.status = 'stop'
            self.display('stop', [0,0])

    def red_released(self,x, status=0): 
        self.print('red released')   
                          
    def black(self,x, status=0): 
        self.print('black pressed')
        
        # when ready > start 
        if self.status == 'ready': 
            self.status = 'working'
            if not self.r.MAIN.state: 
                self.r.MAIN.on()
            time.sleep(config.TIME_WAIT_MAIN)
            if not self.b.RIGHT.pressed: 
                self.move = 'right'
                self.r.LEFT.off(); self.r.RIGHT.on()#self.r.H.go(1)
            else: 
                self.move = 'left'
                self.r.RIGHT.off(); self.r.LEFT.on()
            self.display('working', [0,0])
            
        # when working > stop H V but not M and wait 
        elif self.status == 'working': 
            self.status = 'stop'
            self.previous_move = self.move #preserving direction
            self.move = None
            self.r.MAIN.off()
            self.r.UP.off()
            self.r.DOWN.off()
            self.r.LEFT.off()
            self.r.RIGHT.off()
            self.display('stop', [0,0])
            
        # second press when stopped - resume same direction
        elif self.status in ('stop', 'cancelling'): 
            self.status = 'working'
            self.r.MAIN.on()
            if self.previous_move == 'right': 
                self.r.LEFT.off(); self.r.RIGHT.on() #self.r.H.go(1)
                self.move = 'right'
                self.display('working', [0,0])
            elif self.previous_move == 'left': 
                self.r.RIGHT.off(); self.r.LEFT.on() #self.r.H.go(0)
                self.move = 'left'
                self.display('working', [0,0])
            elif self.previous_move == 'down': 
                # do not go more down 
                if self.b.LEFT.pressed: 
                    self.r.RIGHT.on() #self.r.H.go(1)
                    self.move = 'right'
                    self.display('working', [0,0])
                elif self.b.RIGHT.pressed: 
                    self.r.LEFT.on() #self.r.H.go(0)
                    self.move = 'left'
                    self.display('working', [0,0])
                else: # default go right # right not pressed
                    self.r.RIGHT.on() 
                    self.move = 'right'
                    self.display('working', [0,0])
            elif self.previous_move == 'return 00': 
                self.return_top()
            

    def black_released(self,x, status=0): 
        self.print('black released')   
    
    def ready(self): 
        self.display('ready', [0, 0])
        time.sleep(config.TIME_READY)
        self.status = 'ready'
    
    def finish(self): 
        self.status = 'finishing'
        self.display('finishing', [0, 0])
        self.r.MAIN.off()
        time.sleep(config.TIME_FINISH)
        self.return_top()
                                              
    
if __name__ == '__main__': 
    from relay import RELAY
    from btn import Button
    from log import LOG
    
    log = LOG(config.LOG)
    
    r1 = RELAY(pins.R1, name='LEFT', id='LEFT', debug = config.DEBUG, \
               wait = dict(on=config.TIME_WAIT_LEFT_ON, off=config.TIME_WAIT_LEFT_OFF), \
               tags = ['   ', 'LFT'], d = None, pos = [0*8, 30], log=log )
               
    r2 = RELAY(pins.R2, name='RIGHT', id='RIGHT', debug = config.DEBUG, \
               wait = dict(on=config.TIME_WAIT_RIGHT_ON, off=config.TIME_WAIT_RIGHT_OFF), \
               tags = ['   ', 'RGT'], d = None, pos = [4*8, 30], log=log )
    
    r3 = RELAY(pins.R3, name='UP', id='UP', debug = config.DEBUG, \
               wait = dict(on=config.TIME_WAIT_UP_ON, off=config.TIME_WAIT_UP_OFF), \
               tags = ['   ', 'UP'], d = None, pos = [8*8, 30], log=log)
               
    r4 = RELAY(pins.R4, name='DOWN', id='DOWN', debug = config.DEBUG, \
               wait = dict(on=config.TIME_WAIT_DOWN_ON, off=config.TIME_WAIT_DOWN_OFF), \
               tags = ['   ', 'DWN'], d = None, pos = [12*8, 30], log=log)
               
    r5 = RELAY(pins.R5, name='MAIN', id='MAIN',\
               wait = dict(on=config.TIME_WAIT_MAIN_ON, off=config.TIME_WAIT_MAIN_OFF), \
               tags = ['    ', 'MAIN'], d = None, pos = [16*8, 30], log=log)
    
    p = PILLY(log=log)
    
    b1 = Button(pin=Pin(pins.B1, mode=Pin.IN, pull=Pin.PULL_UP), \
                callback=p.left, release_callback = p.left_released, \
                min_ago = config.WAIT_BETWEEN_PRESSED_MS, \
                id = 'LEFT', d = None, pos = [0,1], log=log)

    b2 = Button(pin=Pin(pins.B2, mode=Pin.IN, pull=Pin.PULL_UP), \
                callback=p.right, release_callback = p.right_released, \
                min_ago = config.WAIT_BETWEEN_PRESSED_MS, \
                id = 'RIGHT', d = None, pos = [2,1], log=log )

    b3 = Button(pin=Pin(pins.B3, mode=Pin.IN, pull=Pin.PULL_UP), \
                callback=p.top, release_callback = p.top_released, \
                min_ago = config.WAIT_BETWEEN_PRESSED_MS, \
                id = 'TOP', d = None, pos = [4,1], log=log )

    b4 = Button(pin=Pin(pins.B4, mode=Pin.IN, pull=Pin.PULL_UP), \
                callback=p.bottom, release_callback = p.bottom_released, \
                min_ago = config.WAIT_BETWEEN_PRESSED_MS, 
                id = 'BOTTOM', d = None, pos = [6,1], log=log )

    red = Button(pin=Pin(pins.B5, mode=Pin.IN, pull=Pin.PULL_UP), \
                callback=p.red, release_callback = p.red_released, \
                min_ago = config.WAIT_BETWEEN_PRESSED_MS, \
                id = 'RED', d = None, pos = [8,1], log=log )

    black = Button(pin=Pin(pins.B6, mode=Pin.IN, pull=Pin.PULL_UP), \
                callback=p.black, release_callback = p.black_released, \
                min_ago = config.WAIT_BETWEEN_PRESSED_MS, \
                id = 'BLACK', d = None, pos = [10,1], log=log )

    p.hook_pereferials(btns=[b1, b2, b3, b4, red, black], \
                       relays=[r1,r2,r3,r4,r5])
             
    p.initialize()








