import network
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect('WFA-4', 'impervious589') # connect to an AP
wlan.ifconfig(('192.168.1.103', '255.255.255.0', '192.168.1.1', '8.8.8.8'))
