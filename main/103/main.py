# main for 103

from esp_lib import wifi_connect #do_connect_with_display, failback
from time import sleep
from machine import reset, Pin
import secrets
from oled import oled_spi
import pins, config
from temp_ds18b20 import DS18X20
from common import TIME, OBJECT, are_you_alive, reset_yourself#, cpu_freq, deep_sleep
from rgb_led import RGB_LED
import gc
from http_control import loop
import _thread
from btn import Button

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

# BTN 
def test1(x, status=True):
    print('test1 ' + str(x) + ' ' + str(status))

def test1_release(x, status=False): 
    print('test1 release ' + str(x) + ' ' + str(status))    

        
b1 = Button(pin=Pin(pins.B1, mode=Pin.IN, pull=Pin.PULL_UP), callback=test1, release_callback=test1_release, min_ago = 2000, id = 'B1', d=d, pos=[0,30] )

def run(): 
    "run cycle"
    # time 
    now = tm.string()
    if now.endswith('00'):
        d.fill(0)    
        
    # temperature
    tmp, tmp_measured = temp.apiTrue()
    d.fill_rect(0, 10, 128, 10, 0); d.text('temp ' + str(tmp), 0, 10, 1)
    if tmp_measured:
        rgb.color('blue' if tmp != 0 else 'red')
    d.fill_rect(0, 20, 128, 10, 0); d.text('time ' + now, 0, 20, 1)
    
    # memory
    _g =  gc.mem_free()
    d.fill_rect(0, 60, 128, 5, 0)
    d.fill_rect(0, 60, int(_g * 128 / gc_total) % 128, 5, 1)
    
    print('RAM ' + str(int(_g/1024)) + ' of ' + str(int(gc_total/1024))  + ', temp = ' + str(tmp) + (' * ' if tmp_measured else ''))
    d.show()
    if tmp_measured: 
        rgb.color('off')


def testThread():
    global stop 
    while True:
        if stop: return 
        run()
        sleep(config.SLEEP)
    
if __name__ == '__main__':
    _thread.start_new_thread(testThread, ())
    loop(d)
    # test will be  http://192.168.1.103/rgb/blue
    # test          http://192.168.1.103/temp/0