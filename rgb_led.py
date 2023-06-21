
from pins import RED, BLUE, GREEN
from  machine import Pin

import __main__ as m

class RGB_LED():
    def __init__(self, init = 'off'):
        self.pins = [Pin(int(i), Pin.OUT) for i in  [RED,BLUE,GREEN]]
        self.colors ={'off'     : [0,0,0],
                      'white'   : [1,1,1],
                      'red'     : [1,0,0],
                      'green'   : [0,1,0],
                      'blue'    : [0,0,1],
                      'yellow'  : [1,1,0],
                      'cyan'    : [0,1,1],
                      'magneta' : [1,0,1]
                      }
        self.color(init)
    def color(self, rgb):
        try:
            for col, setting in enumerate(self.colors[rgb]):
                self.pins[col].value(  int( not setting) )
            try:  # here injected exception
                m.states.RF_positions['color'] = rgb
                m.states.previous_color = rgb
            except: pass
            return 'rgb ' + rgb
        except Exception as e:
            print (e)
            return str(e)
    def api(self, value):
        "for http_control"
        return self.color(value[0].lower())