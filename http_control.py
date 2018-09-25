"""ESP http api

adc - analog 1-1024 / 0-3.3v (on current board ! be careful with OLDs 0-1v)

"""
#DONE: GIT
#TODO: split modules, import only needed / memory
#TODO: return json or smth like that
#TODO: external list of pins.


from  machine import Pin
from machine import ADC
adc = ADC(0)

from time import sleep
import json

# defining PINS
from pins import RED, BLUE, GREEN, INTERNAL_LED, RF433, BEEP

html = """HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8

%s
"""


import socket
addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
s = socket.socket()
s.bind(addr)
s.listen(1)

print('listening on', addr)

#TODO:
# machine.reset()
# machine.unique_id()

def control(line):
    try:
        line = line.replace('\\r\\n','').replace(' HTTP','')
        if line.find('control') != -1 or line.find('gpio') != -1: # gpio > compatibility
            print ('control function')
            params = [i for i in line.replace('control','').replace('gpio','').split('/') if i not in ["b'GET ",'',"1.1'"]]
            print (params)
            func, values = params[0], params[1:]
            if func in globals():
                return (func, globals()[func](values)) # here can actually return dict which will be jsonified
            else:
                return (func, 'no funcion registered')
        else:
            return (None,None)
    except Exception as e:
        return ('error', str(e))

def gpio(value):
    "compatibility"
    return pin(value)

def pin(value):
    print ('pin function')
    print ('values recieved ' + str(value))
    try:
        p = Pin(int(value[0]), Pin.OUT)
        if str(value[1]) == '1': p.low()
        if str(value[1]) == '0': p.high()
        return 'OK - ' + str(value)
    except:
        return 'ERROR'

def beep(value):
    "beeper / reverced 1-0"
    if value[0] == '1':
        pin([BEEP,'0'])
    if value[0] == '0':
        pin([BEEP,'1'])
    return 'beeper set to ' + str(value[0])

def sensor(value):
    try:
        current = previous_color
        color(['red',''])
        if len(value)>=1:
            if value[0] == 'sound':
                beep('1')
        r = str(adc.read())
        if len(value)>=1:
            if value[0] == 'sound':
                beep('0')
        color([current,''])

        return (r)
    except Exception as e:
        print (e)
        return str(e)

# color
previous_color = 'off'
def color(value):
    "pins defined in file pins"
    global previous_color
    requested = value[0].lower() #syntax /control/color/red
    colors = {'off'    : [0,0,0],   'white' : [1,1,1],
              'red'    : [1,0,0],   'green' : [0,1,0], 'blue' :     [0,0,1],
              'yellow' :[1,1,0],    'cyan'  : [0,1,1], 'magneta' :  [1,0,1]
              }
    pins = {0:RED, 1:BLUE, 2:GREEN}
    try:
        for col, setting in enumerate(colors[requested]):
            pin([pins[col], str(setting)])
        previous_color = requested
        return 'color set to ' + requested
    except Exception as e:
        print (e)
        return str(e)

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

#%% rf433
def rf433(value):
    """wrapper for _rf433
    [group,what]
    """
    print ('rf warapper: value: ' + str(value))
    com = [1 if value[1] in [1, '1','on','ON','True','true'] else 0][0]
    if value[0] == 'light':
        res = [_rf433([5,com]) ] # old > [_rf433([v,com]) for v in [1,2,3,4]]
    elif value[0] == 'heater':
        res = [_rf433([12,com])]
    elif value[0] == 'coffee':
        res = [_rf433([11,com])]
    elif value[0] == 'all':
        res = [_rf433([v,com]) for v in [5,11,12,21]]
    elif value[0] == 'dimlight':
        # for Philips lamps > ['dimlight', 0] for DIM  / ['dimlight', 1] for BRIGHT
        res = []
        if com == 0:  # bright to dim
            res.append(_rf433([5,0])); sleep (0.5)
            res.append(_rf433([5,1])); sleep (0.5) # now mode 2
            res.append(_rf433([5,0])); sleep (0.5)
            res.append(_rf433([5,1])); sleep (0.5) # now mode 3 (dim)
        else:
            res.append(_rf433([5,0])); sleep (0.5)
            res.append(_rf433([5,1])); sleep (0.5) # now mode 1
    else:
        res = [_rf433([value[0],com])]

    ret= str(value[0]) +'<br>' + '<br>'.join(res)
    return ret

def _rf433(value):
    """[signal, OnOff]
    : 150 - 300 delay good, pin 14 (D5), 5V """
    print ('_rf433' + str(value))
    pin = RF433 #int(value[1])
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
              '13': [
                  [4,2,2,4,4,2,4,2,4,4,4,2,2,2,2,2,2,2,2,2,4,2,4,2,2,2,2,2,4,4,2,4,2,3],
                  [4,2,2,4,4,2,4,2,4,4,4,2,2,2,2,2,2,2,2,2,4,2,4,4,2,2,2,2,4,4,2,2,2,3]
                  ],
              '14': [
                  [4,2,2,4,4,2,4,2,4,4,4,2,2,2,2,2,2,2,2,2,2,4,4,2,2,2,2,2,2,2,4,4,2,3],
                  [4,2,2,4,4,2,4,2,4,4,4,2,2,2,2,2,2,2,2,2,2,4,4,4,2,2,2,2,2,2,4,2,2,3]
                  ],
              '99': [ # all 4
                  [4,2,2,4,4,2,4,2,4,4,4,2,2,2,2,2,2,2,2,2,4,2,2,2,2,2,2,2,4,4,4,2,2,3],
                  [4,2,2,4,4,2,4,2,4,4,4,2,2,2,2,2,2,2,2,2,2,4,2,2,2,2,2,2,2,2,2,4,2,3]
                  ],
              # another module > not used.
              '21': [
                  [1,4,1,4,1,4,1,4,1,1,1,1,1,1,1,1,1,1,1,4,4,4,1,1,4,1,1,4,1,1,4,4,4,4,4,1,1,1,1,4,4,4,4,4,4,4,4,6],
                  [1,4,1,4,1,4,1,4,1,1,1,1,1,1,1,1,1,1,1,4,4,4,1,1,4,1,1,4,1,1,4,4,4,4,4,1,1,1,1,4,4,4,4,4,4,4,4,6]
                  ]
              }
    mapping = {1 : (3,3), 2 : (3,7), 3: (3,92), 4: (7,3), 5 : (7,7), 6 : (7,92)}
    p = Pin(pin , Pin.OUT)

    current = previous_color
    color(['yellow',''])
    #led = Pin(2, Pin.OUT)
    try:
        for n in range(0,8):
            for i in signals[str(signal)][OnOff]:
                p.high()
                #led.high()
                sleep((mapping[i][0] * timeDelay))
                p.low()
                #led.low()
                sleep((mapping[i][1] * timeDelay))
        #led.high()
        sleep(0.2)
        color([current,''])
        return str('signal {} sent to {}'.format(OnOff,signal))
    except Exception as e:
        print (e)
        return str(e)

#%% RUN
try:
    from motor import motor
except Exception as e:
    print (str(e), file=open('log','w'))

pin([INTERNAL_LED,'1']) # indicating on

cnt = {}
message = {}
while True:
    cl, addr = s.accept()
    print('client connected from', addr)
    message['from IP'] = str(addr)
    cl_file = cl.makefile('rwb', 0)
    while True:
        line = cl_file.readline()
#        print (line)
        if not line or line == b'\r\n':
            break
        if line.find(b'Host:')!=-1: message['host'] = str(line).replace('\\r\\n','')
        func, reply = control(str(line))
        if func is not None:
            cnt[func] = reply
    cl.sendall(html % json.dumps({'data':cnt, 'message' : message}))
    cl.close()
    cnt = {}
    message = {}