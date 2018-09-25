#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 25 10:30:31 2018

@author: s84004
"""


def blink(on = 0.2, off = 0.2):
 from time import sleep
 from machine import Pin
 p = Pin(2, Pin.OUT)
 while True:  p.low(); sleep(on); p.high(); sleep(off)


def get_data(URL, ENTITY, API_PASSWORD):
    'request data from url'
    import urequests
    url = '{}{}'.format(URL, ENTITY)
    headers = {'x-ha-access': API_PASSWORD,
               'content-type': 'application/json'}
    resp = urequests.get(url, headers=headers)
    return resp.json()['state']

