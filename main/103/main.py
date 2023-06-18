SLEEP = 1
INTRO = 'HELLO ALEX :)'
SKIP_LOOPS = 30 

from esp_lib import do_connect_with_display, failback
from time import sleep
from machine import reset
import secrets
from oled import oled_spi
import pins
from temp_ds18b20 import DS18X20
from common import TIME
from rgb_led import RGB_LED
import gc

gc.enable()

# onboard LED
led = None #Pin(pins.LED, Pin.OUT)
rgb = RGB_LED('red')

# d.invert(1)

try:
    # display OLED
    d = oled_spi(pins.OLED_MOSI, pins.OLED_DATA, pins.OLED_RESET, None, pins.OLED_SCK, intro=INTRO, rotate = 0)
    # attempt 1
    wifi = do_connect_with_display(IP = secrets.IP1, essid = secrets.ESSID1, password = secrets.PASSWORD1, led = led, display = d, fill=False, attmpts = 40, id = '(1) ')

    # attempt 2
    if not wifi:
        wifi = do_connect_with_display(IP = secrets.IP2, essid = secrets.ESSID2, password = secrets.PASSWORD2, led = led, display = d, fill=True, attmpts = 40, id = '(2) ')

    # no wifi
    if not wifi:
        d.text('no wifi available', 0, 40, 1)
        d.show()
        sleep(2)
        failback(IP = secrets.IP1, essid = secrets.ESSID1, password = secrets.PASSWORD1)
        
except Exception as e:
    try: 
        print(str(e), file=open('log', 'a'))
    except: pass 
    try: 
        d.text('wifi error', 0, 40, 1)
        d.show()
        sleep(2)
    except: 
        pass 
    failback(IP = secrets.IP1, essid = secrets.ESSID1, password = secrets.PASSWORD1)

rgb.color('blue')
sleep(0.5)
if d is not None: d.fill(0); d.show()

# temp 
temp = DS18X20(pin=pins.TEMPERATURE, skip_loops=SKIP_LOOPS)

tm = TIME()

rgb.color('off')
total = gc.mem_alloc() + gc.mem_free() 

# FOR NOW
while True: 
    d.fill(0)
    tmp, tmp_measured = temp.api_skipped()
    d.text('temp ' + str(tmp), 0, 10, 1)
    if tmp_measured: 
        rgb.color('blue' if tmp != 0 else 'red')
    d.text('time ' + tm.string(), 0, 20, 1)
    _g =  gc.mem_free()
    d.fill_rect(0, 60, int(_g * 128 / total) % 128, 5, 1) 
    print('RAM ' + str(int(_g/1024)) + ' of ' + str(int(total/1024))  + ', temp = ' + str(tmp) + (' * ' if tmp_measured else ''))
    d.show()
    rgb.color('off')
    sleep(SLEEP - (0.75 if tmp_measured else 0))