"http://192.168.1.103/control/stop_thread"
"http://192.168.1.103/control/stop_html"

import socket
import json
import __main__ as m 

html = """HTTP/1.1 200 OK
Content-Type: application/json; charset=utf-8

%s
"""

def control(line):
    try:
        line = line.replace('\\r\\n','').replace(' HTTP','')
        if line.find('control') != -1:
            params = [i for i in line.replace('control','').split('/') if i not in ["b'GET ",'',"1.1'"]]
            print ('control ' + str(params) + ' ', end = '')
            # print ('GLOBALS \n' + str(globals()))
            # print ('LOCALS \n' + str(locals()))
            func, values = params[0], params[1:]
            if func in locals():
                if str(locals()[func]).find('function') != -1:
                    # function
                    return (func, locals()[func](values)) # here can actually return dict which will be jsonified
                elif str(locals()[func]).find('object') != -1:
                    # object
                    try:
                        return (func, locals()[func].api(values))
                    except:
                        return (func, 'object found in locals() but cant trigger .api(v)')
            elif func in globals():
                 if str(globals()[func]).find('function') != -1:
                     # function
                     return (func, globals()[func](values)) # here can actually return dict which will be jsonified
                 elif str(globals()[func]).find('object') != -1:
                     # object
                     try:
                         return (func, globals()[func].api(values))
                     except:
                         return (func, 'object found in globals() but cant trigger .api(v)')                   
            else:
                return (func, 'no funcion or object registered in locals / globals')
        else:
            return (None,None)
    except Exception as e:
        return ('error', str(e))

def check_functions(value=[]): 
    "/control/check_functions"
    print ('GLOBALS \n' + str(globals()))
    print ('LOCALS \n' + str(locals()))
    return {'locals': str(locals()), 'globals': str(globals())}
    
def stop_thread(value = []):
    try: 
        m.stop = True 
    except: 
        pass 
    return 'stopping thread'

def stop_http(value=[]): 
    "exiting http loop"
    return 'exiting http loop'

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
        # http control part
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
                    print(reply)
                if func == 'stop_http':  return  
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