# ESP lib
import network
from machine import Pin
from time import sleep

def do_connect(IP, essid, password):
 "old"
 sta_if = network.WLAN(network.STA_IF)
 sta_if.active(False)
 IP = (IP, '255.255.255.0', '192.168.1.1', '8.8.8.8')
 print('connecting to network...', str(IP), essid, password[0] + '...' + password[-1])
 sta_if.active(True)
 sta_if.ifconfig(IP)
 sta_if.connect(essid, password)
 led = Pin(5,Pin.OUT)
 led.on()
 for a in range(0,10):
  print ('.', end = '')
  if sta_if.isconnected():
   led.off()
   print(" connected. network config:", sta_if.ifconfig())
   return led
  sleep(1)
 print(" can NOT connect to network")


def do_connect_with_display(IP, essid, password, led = None, display=None, fill=False):
    "connect, report OLED (display) + LED (pin)"
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(False)
    print('connecting to network...', str(IP), essid, password[0] + '...' + password[-1])
    if display is not None:
        if fill:
            display.fill(0) # clean
        display.text(essid, 0, 10, 1)
        display.show()
    sta_if.active(True)
    if IP is not None: # None - get IP from router
        sta_if.ifconfig(IP)
    sta_if.connect(essid, password)
    if led is not None: led.on()
    for a in range(0,10):
        print ('.', end = '')
        if display is not None:
            display.text('.', a * 4, 20, 1)
            display.show()
        if sta_if.isconnected():
            if led is not None: led.off()
            print(" connected. network config:", sta_if.ifconfig())
            if display is not None:
                display.text('connected', 0, 30, 1)
                display.text(sta_if.ifconfig()[0], 0, 40, 1)
                display.show()
            return True
        sleep(1)
    print(" can NOT connect to network")
    if display is not None:
        display.text('no connection', 0, 30, 1)
        display.show()
    return False

def failback():
    "min wifi"
    import network
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect('WFA-4', 'impervious589') # connect to an AP
    wlan.ifconfig(('192.168.1.101', '255.255.255.0', '192.168.1.1', '8.8.8.8'))
