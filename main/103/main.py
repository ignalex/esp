# main for 103

from esp_lib import wifi_connect #do_connect_with_display, failback
from time import sleep
from machine import reset
import secrets
from oled import oled_spi
import pins, config
from temp_ds18b20 import DS18X20
from common import TIME, OBJECT
from rgb_led import RGB_LED
import gc
from http_control import loop
import _thread

print('103 ready')
stop = False #thread 

# GC
gc.enable()
gc_total = gc.mem_alloc() + gc.mem_free()

led = None #Pin(pins.LED, Pin.OUT)
rgb = RGB_LED('red') # ready to connect

# display
d = oled_spi(pins.OLED_MOSI, pins.OLED_DATA, pins.OLED_RESET, None, pins.OLED_SCK, intro=config.INTRO, rotate = config.ROTATE)

# wifi
if  wifi_connect(networks = secrets.networks, d = d, led = led, attmpts = config.WIFI_ATTEMPTS):
    rgb.color('blue') # connected
    sleep(0.5)
else:
    for x in range(5):
        rgb.color('red'); sleep(1)
        rgb.color('white'); sleep(1)

# temperature
temp = DS18X20(pin=pins.TEMPERATURE, skip_loops=config.SKIP_LOOPS)

# time
tm = TIME()

# ready
rgb.color('off')
if d is not None: d.fill(0); d.show()

states = OBJECT({'RF_positions' : {'color' :  'off',
                                   'sensor' : 0},
                 'previous_color' : 'off'})

def run(): 
    "run cycle"
    d.fill(0)
    tmp, tmp_measured = temp.api()
    d.text('temp ' + str(tmp), 0, 10, 1)
    if tmp_measured:
        rgb.color('blue' if tmp != 0 else 'red')
    d.text('time ' + tm.string(), 0, 20, 1)
    _g =  gc.mem_free()
    d.fill_rect(0, 60, int(_g * 128 / gc_total) % 128, 5, 1)
    print('RAM ' + str(int(_g/1024)) + ' of ' + str(int(gc_total/1024))  + ', temp = ' + str(tmp) + (' * ' if tmp_measured else ''))
    d.show()
    rgb.color('off')


def testThread():
    global stop 
    while True:
        if stop: return 
        run()
        sleep(config.SLEEP)
    
if __name__ == '__main__':
    _thread.start_new_thread(testThread, ())
    loop()
    # test will be  http://192.168.1.103/rgb/blue
    # test          http://192.168.1.103/temp/0