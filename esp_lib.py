# ESP lib

def do_connect(IP, essid, password  ):
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


