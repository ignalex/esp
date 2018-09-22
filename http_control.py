"""ESP http api
current PINS allocation
14 - rf433
15 - beep
2 - internal LED (blue) : set 1 on connect
adc - analog 1-1024 / 0-3.3v (on current board ! be careful with OLDs 0-1v)
16 (D0) - LED RED #TODO: to change - D0 needed for self waking up
5 (D1) -  LED BLUE
4 (D1) -  LED GREEN

#TODO: motor shield used D1 D2 D3 D4
#TODO: waking up uses D0
"""
#DONE: GIT
#TODO: split modules, import only needed / memory
#TODO: return json or smth like that
#TODO: external list of pins.


from  machine import Pin
from machine import ADC
adc = ADC(0)

from time import sleep

html = b"""HTTP/1.1 200 OK
Content-Type: text/html

<!DOCTYPE html>
<html>
    <head> <title>ESP</title> </head>
    <body>%s</body>
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
        if line.find('control') != -1 or line.find('gpio') != -1: # gpio > compatibility
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

def gpio(value):
    "compatibility"
    return pin(value)

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

def beep(value):
    "15 pin is a beeper / reverced 1-0"
    if value[0] == '1':
        pin(['15','0'])
    if value[0] == '0':
        pin(['15','1'])
    return 'beeper set to ' + str(value[0])

def sensor(value):
    try:
        current = previous_color
        color(['magneta',''])
        if len(value)>=1:
            if value[0] == 'sound':
                beep('1')
        r = 'adc='+str(adc.read())
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
    "using pins D0 (16), D1 (5), D2 (4), control RGB (respectively)"
    global previous_color
    requested = value[0].lower() #syntax /control/color/red
    colors = {'off' : [0,0,0], 'white' : [1,1,1],
              'red' : [1,0,0], 'green' : [0,1,0], 'blue' : [0,0,1],
              'yellow' :[1,1,0], 'cyan' : [0,1,1], 'magneta' : [1,0,1]
              }
    pins = {0:16, 1:5, 2:4}
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
pin(['2','1']) # indicating on

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