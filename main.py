from esp_lib import do_connect

# assign IP to ESP, SSID and pass must be given.
do_connect(IP = '192.168.1.175' , essid = 'WFA-4', password = 'impervious589')

#reseting 14 pin > othersiwe it is jamming 433MHz
#from machine import Pin
#from pins import RF433
#p = Pin(RF433 , Pin.OUT)
#p.low()

try:
    import http_control
except Exception as e:
    print (str(e), file=open('log','a'))