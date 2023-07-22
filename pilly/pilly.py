# -*- coding: utf-8 -*-
# motors
#   M1 - main motor (* optionaly + starter)
#   H  - horizontal motor (left / right)
#       HR, HL
#   V  - vertical motor (up / down)
#       VU, VD
#   R   - releys

# control
#   LEFT RIGHT TOP BOTTOM   - limit btns
#   START STOP
#   RELEYS  - powers on relays
#   RESET   - all to start position

# tumblers
#   LOGIC RELEY - logic power ESP, reley powers low voltage releys


class RELAY: 
    self.

class PILLY:
    def __init__(self, btns=None, relays=None): 
        self.btn = btns
        self.relay = relays
        self.position = [None,None] #unknown
        self.status = 'initializing'
        
    def initialize(self):
        for r in self.relays: 
            r.value(0)
            
        if self.position == [None, None]:
            pass
        
        
p = PILLY()


def initialize(return_home = True):
    "on power on"
    "releys to allow"

def start():
    "start at position"
    "reset irq for btns"
    "turn MAIN on"
    "start GoRight"

def stop():
    "stop and wait"
    global WAIT
    WAIT = True
    print(WAIT)

def reset():
    "reset all"

def return_to_zero():
    "set status RETURN"
    "go Left"
    "go Top"

def onRight(s): 
    "stop right"
    "go down s sec"
    "start go Left"
    
def onLeft(s):
    "stop LEFT"
    "go down s sec"
    "start go RIGTH"    

def onDown(): 
    "stop MAIN"
    "return to 0 0"

