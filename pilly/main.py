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
from relay import RELAY, MOTOR
from btn import Button
from dust import DUST

try: 
    r1 = RELAY(pins.R1, 'HORIZONTAL dir', debug = config.DEBUG, \
               wait = dict(on=config.TIME_WAIT_HDIR_ON, off=config.TIME_WAIT_HDIR_OFF))
    r2 = RELAY(pins.R2, 'HORIZONTAL drive', debug = config.DEBUG, \
               wait = dict(on=config.TIME_WAIT_HGO_ON, off=config.TIME_WAIT_HGO_OFF))
    m1 = MOTOR(r1,r2,'H', tags = ['<', '>'], d = d, pos = [0,3])
    
    r3 = RELAY(pins.R3, 'VERTICAL dir', debug = config.DEBUG, \
               wait = dict(on=config.TIME_WAIT_VDIR_ON, off=config.TIME_WAIT_VDIR_OFF))
    r4 = RELAY(pins.R4, 'VERTICAL drive', debug = config.DEBUG, \
               wait = dict(on=config.TIME_WAIT_VGO_ON, off=config.TIME_WAIT_VGO_OFF))
    m2 = MOTOR(r3,r4,'V', tags = ['^', 'v'], d = d, pos = [5,3])
    
    m3 = RELAY(pins.R5, 'M', \
               wait = dict(on=config.TIME_WAIT_MAIN_ON, off=config.TIME_WAIT_MAIN_OFF), \
               d = d, pos = [10, 3])
    
    p = PILLY()
    
    b1 = Button(pin=Pin(pins.B1, mode=Pin.IN, pull=Pin.PULL_UP), \
                callback=p.left, release_callback = p.left_released, \
                min_ago = config.WAIT_BETWEEN_PRESSED_MS, \
                id = 'LEFT', d = d, pos = [0,1] )

    b2 = Button(pin=Pin(pins.B2, mode=Pin.IN, pull=Pin.PULL_UP), \
                callback=p.right, release_callback = p.right_released, \
                min_ago = config.WAIT_BETWEEN_PRESSED_MS, \
                id = 'RIGTH', d = d, pos = [2,1] )

    b3 = Button(pin=Pin(pins.B3, mode=Pin.IN, pull=Pin.PULL_UP), \
                callback=p.top, release_callback = p.top_released, \
                min_ago = config.WAIT_BETWEEN_PRESSED_MS, \
                id = 'TOP', d = d, pos = [4,1] )

    b4 = Button(pin=Pin(pins.B4, mode=Pin.IN, pull=Pin.PULL_UP), \
                callback=p.bottom, release_callback = p.bottom_released, \
                min_ago = config.WAIT_BETWEEN_PRESSED_MS, 
                id = 'BOTTOM', d = d, pos = [6,1] )

    red = Button(pin=Pin(pins.B5, mode=Pin.IN, pull=Pin.PULL_UP), \
                callback=p.red, release_callback = p.red_released, \
                min_ago = config.WAIT_BETWEEN_PRESSED_MS, \
                id = 'RED', d = d, pos = [8,1] )

    black = Button(pin=Pin(pins.B6, mode=Pin.IN, pull=Pin.PULL_UP), \
                callback=p.black, release_callback = p.black_released, \
                min_ago = config.WAIT_BETWEEN_PRESSED_MS, \
                id = 'BLACK', d = d, pos = [10,1] )

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
    