#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Sep 17 16:51:56 2018

@author: AI
"""

import time
from  machine import Pin
from pins import PIN_ENABLE, PIN_STEP, PIN_DIRECTION
from hcsr import HCSR

#%% motor
def motor(value = [5000, 11, 1, 50]):
    """steps (negative for opposite directon), delay - 1/10000 sec, use_hcsr_sensor = 1 (default), 0 = skip
    looks like 11 is a min step (fastest speed)
    calibration: value = [-9999,x] - go all the way down with checking hcsr_sensor state [big enough number]
    """
    try:
        results = {} # in case error in initialisation
        hcsr_sensor = True
        direction, steps = int(int(value[0]) > 0), abs(int(value[0]))

        # delay is 2 arg
        if len(value)>=2:
            delay = int(value[1])
        else:
            delay = 11

        # skips
        if len(value)>=3:
            if int(value[2]) == 0:
                hcsr_sensor = False

        # skip
        if len(value)>=4:
            skips_ = int(value[3])
        else:
            skips_ = 50

        results = {'steps' : steps, 'direction' : direction,
                  'steps_done' : 0, 'hcsr_sensor_obstraction' : False,
                  'delay' : delay, 'error' : '-', 'status': True,
                  'hcsr_sensor' : hcsr_sensor }

        print ('setting pins')
        pin_enable = Pin(PIN_ENABLE, Pin.OUT, 0)
        pin_direction = Pin(PIN_DIRECTION, Pin.OUT, 0)
        pin_step = Pin(PIN_STEP, Pin.OUT, 0)

        print ('pins set')

        pin_enable.low() # LOW is enable
        print ('direction {}, steps {}, delay {}'.format(str(direction), str(steps), str(delay)))

        pin_direction.value(direction)

        print ('GO')
        Z = []
        skips = skips_
        for x in range(0,steps+1):
            # using sensor on the way down every [skips] step
            if hcsr_sensor and skips < 0 and direction == 0:
                read = HCSR(readings=[5,2], limit=300, echo_timeout_us=500*10)
                if read[0]: # sensing obstraction > stop
                    print ('hcsr_sensor disconnected, stopping')
                    results['hcsr_sensor_obstraction'] = True
                    Z.append(read[1]) #!!!: test
                    break
                Z.append(read[1]) #!!!: testt
            skips -= 1
            if skips < -1:
                skips = skips_
            pin_step.high()
            time.sleep(delay/10000)
            pin_step.low()
        print(Z)
        del Z
        print ('stop')

        pin_step.low()
        pin_enable.high() # off - reverse logic
        print ('pins desabled, cycle finished')
        results['steps_done'] = x
        return results
    except Exception as e:
        print (e)
        results['error'] = str(e)
        results['status'] = False
        return results