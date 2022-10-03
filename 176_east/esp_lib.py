# ESP lib 

def do_connect(IP = '192.168.1.175' , essid = 'WFA-4', password = 'impervious589' ):
 import network
 from time import sleep 
 sta_if = network.WLAN(network.STA_IF)
 sta_if.active(False)
 IP = (IP, '255.255.255.0', '192.168.1.1', '8.8.8.8')
 print('connecting to network...', str(IP), essid, password[0] + '...' + password[-1])
 sta_if.active(True)
 sta_if.ifconfig(IP)
 sta_if.connect(essid, password)
 for a in range(0,10): 
  print ('.', end = '')
  if sta_if.isconnected(): 
   print(" connected. network config:", sta_if.ifconfig())
   return 
  sleep(1)
 print(" can NOT connect to network")



def blink(on = 0.2, off = 0.2): 
 from time import sleep
 from machine import Pin
 p = Pin(2, Pin.OUT)
 while True:  p.low(); sleep(on); p.high(); sleep(off)
 
 
def get_data(URL, ENTITY, API_PASSWORD):
    'request data from url'
    import urequests
    url = '{}{}'.format(URL, ENTITY)
    headers = {'x-ha-access': API_PASSWORD,
               'content-type': 'application/json'}
    resp = urequests.get(url, headers=headers)
    return resp.json()['state']

