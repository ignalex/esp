# -*- coding: utf-8 -*-
"""
Created on Sun Sep  9 09:17:23 2018

@author: Alexander Ignatov
"""
import time
from  machine import Pin

pin_go = 1 #TODO: turn off power from motor when not used : relay
pin_direction = 2
pin_power_motor = 3 # ???

pin_sensor_lazer = 4
pin_lazer = 5 # or can be used pin_go

PIN_DERECTION = Pin(pin_direction, Pin.OUT)
PIN_POWER_MOTOR = Pin(pin_power_motor, Pin.OUT)
PIN_LAZER = Pin(pin_lazer, Pin.OUT)
PIN_SENSOR_LAZER = Pin(pin_sensor_lazer, Pin.IN, Pin.PULL_UP)

TIME_UP = 5 #TODO: calibrate !!!

def motor(up_down):
    "go up / go down"
    if up_down == 'down' :
        go_down()
    else: # go down all the way and up
        go_down() # for calibrating
        go_up()

def go_down():
    "go down until no lazer (all the way down)"
    set_lazer(1); time.sleep(0.01)
    if lazer() == False: # already down
        return
    motor_cycle(True, 'down')
    while lazer():
        time.sleep(0.01)
    motor_cycle(False)
    set_lazer(0)
    return

def go_up():
    'go up for time'
    motor_cycle(True, 'up')
    time.sleep(TIME_UP)
    motor_cycle(False)
    return


def motor_cycle(onoff, direction='down'):
    if onoff:
        if direction == 'up':
            PIN_DERECTION.low()
        else:
            PIN_DERECTION.high()
        PIN_POWER_MOTOR.high()
    else:
        PIN_POWER_MOTOR.low()

def set_lazer(onoff):
    if onoff:
        PIN_LAZER.high()
    else:
        PIN_LAZER.low()

def lazer():
    lazer_status = PIN_SENSOR_LAZER.value()
    # TODO: what if wrong radings??? (need check!)
    return lazer_status
