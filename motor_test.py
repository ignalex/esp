#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 17 16:51:56 2018

@author: s84004
"""

import time
from  machine import Pin

def motor(direction=0, duration=3):
    "dir 1 / 0, duration - sec"
    pin_enable = 16 # D0 #TODO: change later
    pin_direction = 5 # D1
    pin_power_motor = 4 # D2

    PIN_GO = Pin(pin_enable, Pin.OUT)
    PIN_DERECTION = Pin(pin_direction, Pin.OUT)
    PIN_POWER_MOTOR = Pin(pin_power_motor, Pin.OUT)

    PIN_GO.low() # or high? - reverce logic

    print (direction + str(direction))

    if direction:
        PIN_DERECTION.high()
    else:
        PIN_DERECTION.low()

    print ('motor ON')
    PIN_POWER_MOTOR.high()

    time.sleep(duration)

    print ('motor OFF')

    PIN_POWER_MOTOR.low()
    PIN_GO.high()