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

class OBJECT (object):
    "basic empty object"
    def __init__(self,d={}):
        for k,v in d.items():
            setattr(self,k,v)