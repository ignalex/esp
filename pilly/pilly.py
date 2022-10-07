# -*- coding: utf-8 -*-
# motors
#   M1 - main motor (* optionaly + starter)
#   H  - horizontal motor (left / right)
#       HR, HL
#   V  - vertical motor (up / down)
#       VU, VD
#   R   - releys

# control
#   LEFT RIGHT TOP BOTTOM   - limit btns
#   START STOP
#   RELEYS  - powers on relays
#   RESET   - all to start position

# tumblers
#   LOGIC RELEY - logic power ESP, reley powers low voltage releys

# test

def initialize(return_home = True):
    "on power on"
    "releys to allow"

def start():
    "start at position"
    "reset irq for btns"

def stop():
    "stop and wait"

def reset():
    "reset all"

def return_to_zero():
    "return to 0,0"

def go_step(direction):
    "go"

def go_direction_all_way(motor, direction, stop_main=True):
    "motor all the way till btn interruption"

def main_motor():
    "start stop logic"

def on_left_limit(params):
    "left btn"

def on_right_limit(params):
    "right btn"

def go_down(ms):
    "go down"

def final_stop():
    "stop all, go home"