# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 18:15:22 2020

@author: alexander
"""
import machine 
import dht 
from time import sleep 
from pins import DHT


class DHT11(): 
    def __init__(self): 
        self.d = dht.DHT11(machine.Pin(DHT))
    def measure(self, attempts = 1, delay = 0.01): 
        current = []
        for a in range(0,attempts): 
            try: 
                self.d.measure()
                current.append([self.d.temperature(), self.d.humidity()])
            except: 
                a = a-1 
            sleep(delay if attempts >1 else 0)
        return {'temperature': sum([i[0] for i in current])/attempts, 
                'humidity' :   sum([i[1] for i in current])/attempts}
    def api(self, value): 
        return self.measure()
