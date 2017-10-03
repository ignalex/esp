from esp_lib import do_connect

# assign IP to ESP, SSID and pass must be given.
do_connect(IP = '192.168.1.176' , essid = 'WFA-4', password = 'hidden')
from machine import Pin

#reseting 14 pin > othersiwe it is jamming 433MHz
p = Pin(14 , Pin.OUT)
p.low()

import http_control1
