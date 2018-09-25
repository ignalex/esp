#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 17 16:51:56 2018

@author: AI
"""

import time
from  machine import Pin
from pins import PIN_ENABLE, PIN_STEP, PIN_DIRECTION, PIN_LAZER, PIN_LAZER_SENSOR

#%% motor
def motor(value = [5000, 11, 1]):
    """steps (negative for opposite directon), delay - 1/10000 sec, use_lazer = 1 (default), 0 = skip
    looks like 11 is a min step (fastest speed)
    calibration: value = [-9999,x] - go all the way down with checking lazer state [big enough number]
    """
    try:
        results = {} # in case error in initialisation
        lazer = True
        direction, steps = int(int(value[0]) > 0), abs(int(value[0]))

        # delay is 2 arg
        if len(value)>=2:
            delay = int(value[1])
        else:
            delay = 11

        # skip lazer (0) is 3rd arg
        if len(value)>=3:
            if int(value[2]) == 0:
                lazer = False

        results = {'steps' : steps, 'direction' : direction,
                  'steps_done' : 0, 'lazer_disconnected' : False,
                  'delay' : delay, 'error' : '-', 'status': True,
                  'lazer' : lazer }

        pin_lazer_sensor = 4   # S03

        print ('setting pins')
        pin_enable = Pin(PIN_ENABLE, Pin.OUT)
        pin_direction = Pin(PIN_DIRECTION, Pin.OUT)
        pin_step = Pin(PIN_STEP, Pin.OUT)
        if lazer:
            pin_lazer = Pin(PIN_LAZER, Pin.OUT)
            pin_lazer_sensor = Pin(PIN_LAZER_SENSOR, Pin.IN, Pin.PULL_UP) #???: maybe down?
        print ('pins set')

        pin_enable.low() # or high? - reverse logic
        print ('direction {}, steps {}, delay {}'.format(str(direction), str(steps), str(delay)))

        if direction: # up
            pin_direction.high()
        else: # down -- autostop
            pin_direction.low()
            if lazer: PIN_LAZER.high() # lazer ON

        print ('GO')
        for x in range(0,steps+1):
            # ONLY going down and NO light and NOT skip commanded - STOP
            if direction == 0 and lazer:
                if pin_lazer_sensor.value() == 0:
                    print ('lazer disconnected, stopping')
                    results['lazer_disconnected'] = True
                    break
            pin_step.high()
            time.sleep(delay/10000)
            pin_step.low()

        print ('stop')

        pin_step.low()
        pin_enable.high() # off - reverse logic
        if lazer: pin_lazer.low()   # off
        print ('pin desabled, cycle finished')
        results['steps_done'] = x
        return results
    except Exception as e:
        print (e)
        results['error'] = str(e)
        results['status'] = False
        return results