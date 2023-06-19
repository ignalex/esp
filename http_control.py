#dont call it http

import socket
import json

html = """HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8

%s
"""

def control(line):
    try:
        line = line.replace('\\r\\n','').replace(' HTTP','')
        if line.find('control') != -1:
            params = [i for i in line.replace('control','').split('/') if i not in ["b'GET ",'',"1.1'"]]
            print ('control ' + str(params))
            func, values = params[0], params[1:]
            if func in globals():
                if str(globals()[func]).find('function') != -1:
                    # function
                    return (func, globals()[func](values)) # here can actually return dict which will be jsonified
                elif str(globals()[func]).find('object') != -1:
                    # object
                    # has to have method 'api' accepting 1 array param
                    try:
                        return (func, globals()[func].api(values))
                    except:
                        return (func, 'object found but cant trigger .api(v)')
            else:
                return (func, 'no funcion or object registered')
        else:
            return (None,None)
    except Exception as e:
        return ('error', str(e))


def loop():
    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]
    s = socket.socket()
    #s.settimeout(None)
    s.bind(addr)
    s.listen(10) # was 4
    print('listening on', addr)

    cnt = {}
    message = {}
    while True:
        try:
            cl, addr = s.accept()
            # print('client connected from', addr)
            message['from IP'] = str(addr)
            cl_file = cl.makefile('rwb', 0)
            while True:
                line = cl_file.readline()
                if not line or line == b'\r\n':
                    break
                if line.find(b'Host:')!=-1: message['host'] = str(line).replace('\\r\\n','')
                func, reply = control(str(line))
                if func is not None:
                    cnt[func] = reply
            cl.sendall(html % json.dumps({ 'data':cnt, 'message' : message}))
            cl.close()
            cnt = {}
            message = {}
        except Exception as e:
            try:
                cl.close()
                cnt = {}
                message = {}
            except:
                pass
            print (str(e))

if __name__ == '__main__':
    loop()