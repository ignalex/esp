# -*- coding: utf-8 -*-
"""
Created on Tue May 23 17:55:05 2017

@author: 84004
"""

import socket
addr_info = socket.getaddrinfo("towel.blinkenlights.nl", 23)
addr = addr_info[0][-1]
s = socket.socket()
s.connect(addr)
while True:   
     print(str(s.recv(500), 'utf8'), end='')
