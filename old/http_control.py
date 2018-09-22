from  machine import Pin
p2 = Pin(2, Pin.OUT)
p2.low()

from machine import ADC

adc = ADC(0)

html = """<!DOCTYPE html>
<html>
    <head> <title>some title</title> </head>
    <body>
        %s
    </body>
</html>
"""


import socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)

def control(line, keys = []): 
    if True in [True if line.find(k) !=-1 else False for k in keys]: 
        if line.find('/gpio/0') != -1: 
            p2.high()
            r = 'high'
        elif line.find('/gpio/1') != -1: 
            p2.low()
            r = 'low'
        elif line.find('sensor') != -1: 
            r = str(adc.read())
            return (r)
        return ('found ' + ''.join([k if line.find(k) !=-1 else '' for k in keys]) + ' ' + r ) 
cnt = []
while True:
    cl, addr = s.accept()
    print('client connected from', addr)
    cl_file = cl.makefile('rwb', 0)
    while True:
        line = cl_file.readline()
        if not line or line == b'\r\n': break
        cnt.append( control(str(line), ['/gpio/1' ,'/gpio/0','/sensor']) ) 
    response = html % ''.join([i for i in cnt if i is not None])
    cl.send(response)
    cl.close()
    cnt = []