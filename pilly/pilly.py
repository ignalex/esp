# -*- coding: utf-8 -*-

#TODO: init class first, add relays, add btns (pass callbacks)

class PILLY:
    def __init__(self, btns=[], relays=[], d=None): 
        "b, r - reserverd for [b1,...], [r1,..,m1...]"
        self.d = d # display 
        self.b = []
        for b in btns: 
            setattr(self,b.name,b)
            self.b.append(b)
            
        self.r = []
        for r in relays: 
            setattr(self,r.name,r)
            self.r.append[r]
        
        self.position = [None,None] #unknown
        self.status = 'initializing'
        self.initialize()
        
    def display(self, text, pos): 
        if self.d is not None: 
            self.d.fill_rect(self.pos[0], self.pos[1], len(text) * 10, 10, 0) 
            self.d.text(text, self.pos[0], self.pos[1], 1)
            self.d.show()
        print(text)
            
    def initialize(self):
        for r in self.r: 
            r.off()
            
        if self.position == [None, None]:
            self.return00()
            
        self.display('initialized', [0, 0])
        
    
    def return00(self): 
        "return to 00 from unknown"    
        self.position = [0,0]


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
    
if __name__ == '__main__': 
    p = PILLY()









