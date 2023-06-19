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
    def now(self):
        return self.rtc.datetime()

class OBJECT (object):
    "basic empty object"
    def __init__(self,d={}):
        for k,v in d.items():
            setattr(self,k,v)