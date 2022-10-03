#on 1st bood

import network
IP = ('192.168.1.102', '255.255.255.0', '192.168.1.1', '8.8.8.8')
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.ifconfig(IP)
wlan.connect('WFA-4', '--')
