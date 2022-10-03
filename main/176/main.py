from esp_lib import do_connect


do_connect(IP = '192.168.1.176' , essid = 'WFA-4', password = 'impervious589')

from common import OBJECT
states = OBJECT({'RF_positions' : {'color' :  'off', 
                                   'sensor' : 0}, 
                 'previous_color' : 'off'})

from rgb_led import RGB_LED
color = RGB_LED()

from http_control import loop 
loop()