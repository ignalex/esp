# main for pilly 

from esp_lib import wifi_connect
from time import sleep
from machine import Pin
import secrets
from oled import oled_spi
import pins
import config 

# onboard LED
led = Pin(pins.LED, Pin.OUT)

# display OLED
d = oled_spi(pins.OLED_MOSI, pins.OLED_DATA, pins.OLED_RESET, None, pins.OLED_SCK, intro=config.HELLO, rotate = pins.OLED_ROTATE)
    
# wifi
if  wifi_connect(networks = secrets.networks, d = d, led = led, attmpts = config.WIFI_ATTEMPTS):
    led.off() # connected
else:
    for x in range(10):
        led.off(); sleep(0.2)
        led.on(); sleep(0.2) 

sleep(0.5)
d.fill(0)

from pilly import PILLY
from relay import RELAY
from btn import Button
from dust import DUST
from log import LOG 

log = LOG(config.LOG)

try: 
    r1 = RELAY(pins.R1, name='LEFT', id='LEFT', debug = config.DEBUG, \
               wait = dict(on=config.TIME_WAIT_LEFT_ON, off=config.TIME_WAIT_LEFT_OFF), \
               tags = ['   ', 'LFT'], d = d, pos = [0*8, 30], log=log)
               
    r2 = RELAY(pins.R2, name='RIGHT', id='RIGHT', debug = config.DEBUG, \
               wait = dict(on=config.TIME_WAIT_RIGHT_ON, off=config.TIME_WAIT_RIGHT_OFF), \
               tags = ['   ', 'RGT'], d = d, pos = [4*8, 30], log=log)
    
    r3 = RELAY(pins.R3, name='UP', id='UP', debug = config.DEBUG, \
               wait = dict(on=config.TIME_WAIT_UP_ON, off=config.TIME_WAIT_UP_OFF), \
               tags = ['   ', 'UP'], d = d, pos = [8*8, 30], log=log)
               
    r4 = RELAY(pins.R4, name='DOWN', id='DOWN', debug = config.DEBUG, \
               wait = dict(on=config.TIME_WAIT_DOWN_ON, off=config.TIME_WAIT_DOWN_OFF), \
               tags = ['   ', 'DWN'], d = d, pos = [11*8, 30], log=log)
               
    r5 = RELAY(pins.R5, name='MAIN', id='MAIN',\
               wait = dict(on=config.TIME_WAIT_MAIN_ON, off=config.TIME_WAIT_MAIN_OFF), \
               tags = [' ', 'M+'], d = d, pos = [14*8, 30], log=log)
    
    p = PILLY()
    
    b1 = Button(pin=Pin(pins.B1, mode=Pin.IN, pull=Pin.PULL_UP), \
                callback=p.left, release_callback = p.left_released, \
                min_ago = config.WAIT_BETWEEN_PRESSED_MS, \
                id = 'LEFT', d = d, pos = [0,10], log=log)

    b2 = Button(pin=Pin(pins.B2, mode=Pin.IN, pull=Pin.PULL_UP), \
                callback=p.right, release_callback = p.right_released, \
                min_ago = config.WAIT_BETWEEN_PRESSED_MS, \
                id = 'RIGHT', d = d, pos = [0,10], log=log)

    b3 = Button(pin=Pin(pins.B3, mode=Pin.IN, pull=Pin.PULL_UP), \
                callback=p.top, release_callback = p.top_released, \
                min_ago = config.WAIT_BETWEEN_PRESSED_MS, \
                id = 'TOP', d = d, pos = [0,10], log=log)

    b4 = Button(pin=Pin(pins.B4, mode=Pin.IN, pull=Pin.PULL_UP), \
                callback=p.bottom, release_callback = p.bottom_released, \
                min_ago = config.WAIT_BETWEEN_PRESSED_MS, 
                id = 'BOTTOM', d = d, pos = [0,10], log=log)

    red = Button(pin=Pin(pins.B6, mode=Pin.IN, pull=Pin.PULL_UP), \
                callback=p.red, release_callback = p.red_released, \
                min_ago = config.WAIT_BETWEEN_PRESSED_MS, \
                id = 'RED', d = d, pos = [0,10], log=log)

    black = Button(pin=Pin(pins.B5, mode=Pin.IN, pull=Pin.PULL_UP), \
                callback=p.black, release_callback = p.black_released, \
                min_ago = config.WAIT_BETWEEN_PRESSED_MS, \
                id = 'BLACK', d = d, pos = [0,10], log=log)

    p.hook_pereferials(btns=[b1, b2, b3, b4, red, black], \
                       relays=[m1,m2,m3])
             
    p.initialize()
    
except Exception as e: 
    print(f'cant initialize PILLY class : {str(e)}')

# main loop 
a = 0
while True:
    if a % 10 == 0 and config.DUST:
        dust_ = DUST(50)
        du =str(round(dust_['density'], 1)) + ' [' + str(int(dust_['max_'])) + ']'
        d.text(du,4,10,1)
        d.show()
    a += 1
    if a == 100: a = 0
    sleep(config.SLEEP)
    