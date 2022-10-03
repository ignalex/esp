#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 15:09:35 2022
@author: alexander
https://microcontrollerslab.com/joystick-module-raspberry-pi-pico/
"""

from machine import Pin, ADC
from time import sleep

VRX = ADC(Pin(27))
VRY = ADC(Pin(26))
SW = Pin(25,Pin.IN, Pin.PULL_UP)

while True:
    xAxis = VRX.read_u16()
    yAxis = VRY.read_u16()
    switch = SW.value()

    print("X-axis: " + str(xAxis) + ", Y-axis: " + str(yAxis) + ", Switch " + str(switch))
    if switch == 0:
        print("Push button pressed!")
    print(" ")
    sleep(1)