#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 07:38:13 2023
temperature sensor on 1wire
@author: AI
"""

import time
import machine
import onewire, ds18x20

class DS18X20():
    "temp sensor 1 wire"
    def __init__(self, pin=32, skip_loops = 10, attempts = 1, delay_ms = 10, sleep_ms = 750):
        self.skip_loops = skip_loops
        self.skipped = skip_loops # 1st read
        self.attempts = attempts
        self.delay_ms = delay_ms
        self.sleep_ms = sleep_ms
        self.last_reading = None
        self.ds = ds18x20.DS18X20(onewire.OneWire(machine.Pin(pin)))
        self.roms = self.ds.scan()
        if len(self.roms) == 0:
            print('error initiation DS18X20')
        else:
            print('1wire temp initiated on '+ str(pin))
    def measure(self):
        current = []
        for a in range(0,self.attempts):
            try:
                self.ds.convert_temp()
                time.sleep_ms(self.sleep_ms)
                current.append(self.ds.read_temp(self.roms[0]))
            except:
                a = a-1
            time.sleep_ms(self.delay_ms if self.attempts >1 else 0)
        return round(sum([i for i in current])/self.attempts, 1)
    def api(self, value=[]):
        "massure real if value == [0] or buffered"
        "return buffered N times, or re-measure "
        if type(value) == list:
            if len(value) > 0:
                if str(value[0]) == '0':
                    self.skipped = self.skip_loops # trigger to re-read
        if self.skipped >= self.skip_loops:
            self.skipped = 0
            self.last_reading = self.measure()
        else:
            self.skipped += 1
        return self.last_reading 
    
    def apiTrue(self, value=[]):
        "return Temp, Skipped"
        return [self.api(value), self.skipped == 0]


if __name__ == '__main__':
    t = DS18X20()
    print(t.measure())