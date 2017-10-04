"ESP http api"
#TODO: GIT

from  machine import Pin
from time import sleep

html = b"""<!DOCTYPE html>
<html>
    <head> <title>ESP contrl</title> </head>
    <body> <h1>ESP</h1>
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



def control(line):
    reply = []
    try:
        line = line.replace('\\r\\n','').replace(' HTTP','')
        if line.find('control') != -1 or line.find('gpio') != -1: # gpio > compatibility wiht older versions
            print ('control function')
            reply.append('control function\n')
            params = [i for i in line.replace('control','').replace('gpio','').split('/') if i not in ["b'GET ",'',"1.1'"]]
            print (params)
            func, values = params[0], params[1:]
            if func in globals():
                reply.append( globals()[func](values))
            else:
                reply.append('no func '+str(func)+' registered')
    except Exception as e:
        reply.append(e)
    return '\n'.join(reply)

def pin(value):
    print ('pin function')
    print ('values recieved ' + str(value))
    try:
        p = Pin(int(value[0]), Pin.OUT)
        if value[1] == '1': p.low()
        if value[1] == '0': p.high()
        return 'OK - ' + str(value)
    except:
        return 'ERROR'

def are_you_alive(value):
    return 'I am alive'

def cpu_freq(value = ['80']):
    "80 or 160"
    import machine
    try:
        machine.freq(int(value[0])* 1000000 )
        return 'CPU changed to ' + str(machine.freq())
    except Exception as e:
        print (e)
        return str(e)

def deep_sleep(value = ['10']):
    'to use it, need to connect RST to D0'
    import machine
    try:
        rtc = machine.RTC()
        rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
        rtc.alarm(rtc.ALARM0, int(value[0]) * 1000)
        print('going to sleep for ' + str(value[0]) + ' sec')
        machine.deepsleep()
    except Exception as e:
        print (e)
        return str(e)


def rf433(value):
    """wrapper for _rf433
    [group,what]
    """
    print ('rf warapper: value: ' + str(value))
    com = [1 if value[1] in [1, '1','on','ON'] else 0][0]
    if value[0] == 'light':
        res = [_rf433([5,com]) ] # old > [_rf433([v,com]) for v in [1,2,3,4]]
    elif value[0] == 'heater':
        res = [_rf433([12,com])]
    elif value[0] == 'coffee':
        res = [_rf433([11,com])]
    elif value[0] == 'all':
        res = [_rf433([v,com]) for v in [1,2,3,4,11,12,21]]
    else:
        res = [_rf433([value[0],com])]
    ret= str(value[0]) +'<br>' + '<br>'.join(res)
    return ret


def _rf433(value):
    """[signal, OnOff]
    : 150 - 300 delay good, pin 14 (D5), 5V """
    print ('_rf433' + str(value))
    pin = 14 #int(value[1])
    timeDelay = 200 / 1000000 #float(value[0])/1000000
    signal = value[0]
    OnOff  = int(value[1])
    signals= {'1' : [
                  [2,4,2,4,2,2,2,2,4,2,4,2,4,4,2,4,2,2,2,2,2,4,4,4,2,2,2,2,2,4,4,2,3],
                  [2,4,2,4,2,2,2,2,4,2,4,2,4,4,2,4,2,2,2,2,4,4,4,4,2,2,2,2,4,2,4,2,3]
                  ],
              '2':  [
                  [2,4,2,4,2,2,2,2,4,2,4,2,4,4,2,4,2,2,2,2,2,2,4,4,2,2,2,2,2,2,2,4,3],
                  [2,4,2,4,2,2,2,2,4,2,4,2,4,4,2,4,2,2,2,2,4,2,4,4,2,2,2,2,4,4,4,2,3]
                  ],
              '3':  [
                  [2,4,2,4,2,2,2,2,4,2,4,2,4,4,2,4,2,2,2,2,2,4,2,4,2,2,2,2,2,4,2,4,3],
                  [2,4,2,4,2,2,2,2,4,2,4,2,4,4,2,4,2,2,2,2,4,4,2,4,2,2,2,2,4,2,2,4,3]
                  ],
              '4':  [
                  [2,4,2,4,2,2,2,2,4,2,4,2,4,4,2,4,2,2,2,2,2,4,4,2,2,2,2,2,2,4,4,4,3],
                  [2,4,2,4,2,2,2,2,4,2,4,2,4,4,2,4,2,2,2,2,4,4,4,2,2,2,2,2,4,2,4,4,3]
                  ],
              # for all 1-4
              '5':  [
                  [2,4,2,4,2,2,2,2,4,2,4,2,4,4,2,4,2,2,2,2,4,2,2,2,2,2,2,2,4,4,2,2,3],
                  [2,4,2,4,2,2,2,2,4,2,4,2,4,4,2,4,2,2,2,2,2,4,2,2,2,2,2,2,2,4,2,2,3]
                  ],
              '11': [
                  [4,2,2,4,4,2,4,2,4,4,4,2,2,2,2,2,2,2,2,2,4,4,4,2,2,2,2,2,4,2,4,4,2,3],
                  [4,2,2,4,4,2,4,2,4,4,4,2,2,2,2,2,2,2,2,2,4,4,4,4,2,2,2,2,4,2,4,2,2,3]
                  ],
              '12': [
                  [4,2,2,4,4,2,4,2,4,4,4,2,2,2,2,2,2,2,2,2,4,4,2,2,2,2,2,2,4,2,2,4,2,3],
                  [4,2,2,4,4,2,4,2,4,4,4,2,2,2,2,2,2,2,2,2,4,4,2,4,2,2,2,2,4,2,2,2,2,3]
                  ],
              '21': [
                  [1,4,1,4,1,4,1,4,1,1,1,1,1,1,1,1,1,1,1,4,4,4,1,1,4,1,1,4,1,1,4,4,4,4,4,1,1,1,1,4,4,4,4,4,4,4,4,6],
                  [1,4,1,4,1,4,1,4,1,1,1,1,1,1,1,1,1,1,1,4,4,4,1,1,4,1,1,4,1,1,4,4,4,4,4,1,1,1,1,4,4,4,4,4,4,4,4,6]
                  ]
              }
    mapping = {1 : (3,3), 2 : (3,7), 3: (3,92), 4: (7,3), 5 : (7,7), 6 : (7,92)}
    p = Pin(pin , Pin.OUT)
    led = Pin(2, Pin.OUT)
    try:
        for n in range(0,8):
            for i in signals[str(signal)][OnOff]:
                p.high()
                led.high()
                sleep((mapping[i][0] * timeDelay))
                p.low()
                led.low()
                sleep((mapping[i][1] * timeDelay))
        led.high()
        sleep(0.2)
        return str('signal {} sent to {}'.format(OnOff,signal))
    except Exception as e:
        print (e)
        return str(e)

#def seq(start, stop, step=1):
#    n = int(round((stop - start)/float(step)))
#    if n > 1:
#        return([start + step*i for i in range(n+1)])
#    else:
#        return([])
#
#def rf433_loop(start, end, step,  pause = 1, rng = 6):
#    for a in seq(start, end, step):
#        for n in range(0,rng):
#            rf433([a,n])
#            sleep(pause)
#


cnt = []
while True:
    cl, addr = s.accept()
    print('client connected from', addr)
    cl_file = cl.makefile('rwb', 0)
    while True:
        line = cl_file.readline()
        if not line or line == b'\r\n': break
        cnt.append( control(str(line)) )
    response = html % '\n'.join([i for i in cnt if i is not None]).replace('\n','<br>')
    cl.send(response)
    cl.close()
    cnt = []