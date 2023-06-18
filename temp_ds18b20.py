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
    def __init__(self, pin=32, skip_loops = 10): 
        self.skip_loops = skip_loops
        self.skipped = skip_loops # 1st read
        self.last_reading = 0
        self.ds = ds18x20.DS18X20(onewire.OneWire(machine.Pin(pin)))
        self.roms = self.ds.scan()
        if len(self.roms) == 0: 
            print('error initiation DS18X20')
        else: 
            print('1wire temp initiated on '+ str(pin))
    def measure(self, attempts = 1, delay_ms = 10): 
        current = []
        for a in range(0,attempts): 
            try: 
                self.ds.convert_temp()
                time.sleep_ms(750)
                current.append(self.ds.read_temp(self.roms[0]))
            except: 
                a = a-1 
            time.sleep_ms(delay_ms if attempts >1 else 0)
        return round(sum([i for i in current])/attempts, 1)
    def api(self, value=1): 
        return self.measure()
    def api_skipped(self, value=1): 
        "return (temp, read/skipped)"
        if self.skipped >= self.skip_loops: 
            self.skipped = 0 
            self.last_reading = self.measure(1)
        else: 
            self.skipped += 1
        return self.last_reading, self.skipped == 0 

if __name__ == '__main__':
    t = DS18X20()
    print(t.measure())