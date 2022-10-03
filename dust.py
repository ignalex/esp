#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 13 15:25:28 2022

@author: alexander
https://github.com/amigcamel/pyGP2Y

PM2.5
density value(μg/m3)	Air quality index
AQI	Air quality level	Air quality evaluation
0-35	0-50	Ⅰ	Excellent
35-75	51-100	Ⅱ	Average
75-115	101-150	Ⅲ	Light pollution
115-150	151-200	Ⅳ	Moderate pollution
150-250	201-300	Ⅴ	Heavy pollution
250-500	≥300	Ⅵ	Serious pullution

"""

import machine
from time import sleep

import pins

# pin setup
LED_PIN = machine.Pin(pins.DUST_LED, machine.Pin.OUT)  # D0
VO_PIN = machine.ADC(machine.Pin(pins.DUST_A))  # A0

# constants
SAMPLING_TIME = 0.00028
DELTA_TIME = 0.00004
SLEEP_TIME = 0.00968
VOC = 0.6
MAX = 0


def calc_volt(val):
    return val * 3.3 / 1024


def calc_density(vo, k=0.5):
    global VOC
    global MAX

    dv = vo - VOC
    if dv < 0:
        dv = 0
        VOC = vo
    density = dv / k * 100
    MAX = max(MAX, density)
    return density


def monitor(sample_size=100, callback=None):
    vals = []
    while True:
        try:
            LED_PIN.value(0)
            sleep(SAMPLING_TIME)
            vals.append(VO_PIN.read())
            sleep(DELTA_TIME)
            LED_PIN.value(1)
            sleep(SLEEP_TIME)
            if len(vals) == sample_size:
                avg = sum(vals) / len(vals)
                volt = calc_volt(avg)
                density = calc_density(volt)
                mv = volt * 1000
                print(
                    "{mv} mV / {density} ug/m3 (Voc={voc}) | Max: {max_} ug/m3".format(  # noqa
                        mv=mv,
                        density=density,
                        voc=VOC,
                        max_=MAX,
                    )
                )
                vals = []
                if callback:
                    callback(density)
        except KeyboardInterrupt:
            break
        except Exception:
            raise
        finally:
            LED_PIN.value(0)


def DUST(sample_size=100, callback=None):
    vals = []
    while True:
        try:
            LED_PIN.value(0)
            sleep(SAMPLING_TIME)
            vals.append(VO_PIN.read())
            sleep(DELTA_TIME)
            LED_PIN.value(1)
            sleep(SLEEP_TIME)
            if len(vals) == sample_size:
                avg = sum(vals) / len(vals)
                volt = calc_volt(avg)
                density = calc_density(volt)
                mv = volt * 1000
                print(
                    "{mv} mV / {density} ug/m3 (Voc={voc}) | Max: {max_} ug/m3".format(  # noqa
                        mv=mv,
                        density=density,
                        voc=VOC,
                        max_=MAX,
                    )
                )
                vals = []
                if callback:
                    callback(density)
                return dict(mv=mv, density=density, voc=VOC, max_=MAX)
        except KeyboardInterrupt:
            break
        except Exception:
            raise
        finally:
            LED_PIN.value(0)
