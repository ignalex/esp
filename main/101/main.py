from esp_lib import do_connect_with_display, failback
from time import sleep
from machine import Pin
import secrets
from oled import oled_spi
import pins

# onboard LED
led = Pin(pins.LED, Pin.OUT)

# display OLED
d = oled_spi(pins.OLED_MOSI, pins.OLED_DATA, pins.OLED_RESET, None, pins.OLED_SCK, intro='HELLO PILLY :)', rotate = 180)
# d.invert(1)

try:
    # attempt 1
    wifi = do_connect_with_display(IP = secrets.IP, essid = secrets.ESSID, password = secrets.PASSWORD, led = led, display = d)

    # attempt 2
    if not wifi:
        wifi = do_connect_with_display(IP = secrets.IP2, essid = secrets.ESSID2, password = secrets.PASSWORD2, led = led, display = d, fill=True)

    # no wifi
    if not wifi:
        d.text('no wifi available', 0, 40, 1)
        d.show()
        sleep(2)
except:
    d.text('nwifi error', 0, 40, 1)
    d.show()
    sleep(2)
    failback()

sleep(0.5)
d.fill(0)


from sandbox import count, real_time, relay, Button

real_time(d)

sleep(0.5)

relay
r2 = relay(pins.R2, 1)
r3 = relay(pins.R3, 1)
r4 = relay(pins.R4, 1)
r5 = relay(pins.R5, 1)

d.text('relays initiated', 0, 35, 1)
d.show()

c = 1
def _count(a=None, p=None, counter = 0):
    global c
    d.text(p + ' ' + str(counter), 80, 35, 1)
    d.show()
    #display, a=1, s=1, r = None, cycle=10, stop=False, b = 1, dust=False, a_lim = 128
    count(display=d, a=1, s=0.1 if p == 'B1' else 0.2, r =[r1,r2,r3,r4,r5] if p == 'B1' else [r5, r4, r3, r2, r1], cycle=2, stop=True, b=c, dust=False, a_lim=4)
    # sleep(1)
    c += 1

# min_ago must be ~ > cycle
# PULL_UP better handles static electricity
b1 = Button(pin=Pin(pins.B1, mode=Pin.IN, pull=Pin.PULL_UP), callback=_count, min_ago = 2000, id = 'B1' )
b2 = Button(pin=Pin(pins.B2, mode=Pin.IN, pull=Pin.PULL_UP), callback=_count, min_ago = 2000, id = 'B2' )
b3 = Button(pin=Pin(pins.B3, mode=Pin.IN, pull=Pin.PULL_UP), callback=_count, min_ago = 2000, id = 'B3' )
b4 = Button(pin=Pin(pins.B4, mode=Pin.IN, pull=Pin.PULL_UP), callback=_count, min_ago = 2000, id = 'B4' )
b5 = Button(pin=Pin(pins.B5, mode=Pin.IN, pull=Pin.PULL_UP), callback=_count, min_ago = 2000, id = 'B5' )
b6 = Button(pin=Pin(pins.B6, mode=Pin.IN, pull=Pin.PULL_UP), callback=_count, min_ago = 2000, id = 'B6' )

d.text('btn ready', 0, 45, 1)
d.show()

# # count(d,1, 1, [r1,r2], 4)
while True:
    sleep(2)
    count(d, 1, 1, None, 4, False, c, dust=True)