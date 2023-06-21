# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 18:15:22 2020

@author: alexander
"""
import machine
import ntptime

class TIME() :
    def __init__(self):
        ntptime.settime()
        self.rtc = machine.RTC()
        print('time UTC' + ':'.join([str(i) for i in self.rtc.datetime()[4:7]]))
    def now(self):
        return self.rtc.datetime()
    def string(self, tz = 10):
        hh, mm, ss = self.rtc.datetime()[4:7]
        hh = hh + tz if hh + 10 < 24 else hh + tz - 24
        return ':'.join([ ('' if len(str(i)) == 2 else '0') + str(i) for i in [hh, mm, ss]])
    def api(self, value):
        return self.string()

class OBJECT (object):
    "basic empty object"
    def __init__(self,d={}):
        for k,v in d.items():
            setattr(self,k,v)
            
def are_you_alive(value):
    return 'I am alive'

def reset_yourself(value):
    'reset machine'
    print ('resetting')
    machine.reset()

# def cpu_freq(value = ['80']):
#     "80 or 160"
#     try:
#         machine.freq(int(value[0])* 1000000 )
#         return 'CPU changed to ' + str(machine.freq())
#     except Exception as e:
#         print (e)
#         return str(e)

# def deep_sleep(value = ['10']):
#     'to use it, need to connect RST to D0'
#     try:
#         rtc = machine.RTC()
#         rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
#         rtc.alarm(rtc.ALARM0, int(value[0]) * 1000)
#         print('going to sleep for ' + str(value[0]) + ' sec')
#         machine.deepsleep()
#     except Exception as e:
#         print (e)
#         return str(e)
