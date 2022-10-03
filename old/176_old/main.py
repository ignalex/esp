from esp_lib import do_connect


do_connect(IP = '192.168.1.176' , essid = 'WFA-4', password = 'impervious589')

from common import OBJECT
states = OBJECT({'RF_positions' : {'color' :  'off', 
                                   'sensor' : 0}, 
                 'previous_color' : 'off'})

import http_control