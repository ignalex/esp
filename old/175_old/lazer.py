# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 21:53:07 2018

@author: Alexander Ignatov
"""
from time import sleep
from  machine import Pin
from pins import *
pin_lazer = Pin(PIN_LAZER, Pin.OUT)
pin_lazer.value(1)
pin_lazer_sensor = Pin(PIN_LAZER_SENSOR, Pin.IN, 0)
led = Pin(INTERNAL_LED,Pin.OUT)
while True:
    print(pin_lazer_sensor.value())
    led.value(not pin_lazer_sensor.value())
    sleep(0.2)