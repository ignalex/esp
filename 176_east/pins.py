#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 09:18:42 2018
@author: Alexander Ignatov
"""

#current PINS allocation

# adc - analog 1-1024 / 0-3.3v (on current board ! be careful with OLDs 0-1v)

# LED
RED =           16     # 16 (D0) - LED RED     !!!: conflict D0- waking up
BLUE =          5      # 5 (D1) -  LED BLUE    !!!: conflict
GREEN =         4      # 4 (D2) -  LED GREEN   !!!: conflict

# MOTOR
PIN_ENABLE =    0      # D3
PIN_STEP =      12     # D6
PIN_DIRECTION = 13     # D7
HCSR_TRIGGER =     5      # D1                     !!!: conflict
HCSR_SENSOR = 4   # D2                     !!!: conflict

INTERNAL_LED =  2      # (D4) internal LED (blue) : set 1 on connect
RF433 =         14     # (D5) - rf433
BEEP =          15      # 15 - (D8)- beep

