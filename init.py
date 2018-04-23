#!/usr/bin/env python
# coding: utf8

import socket
import os
import time

def is_connected():
    
    print("**** Init the webserver when            ****")
    print("**** a internet connection is detected  ****")
    
    start = time.time()
    stop_script = 1000 # ten minutes
    is_connected = 0
    while is_connected == 0: #review the optimisation of the loop : event
	try:
	    socket.create_connection(('www.google.fr',80))
	    print "Connected to the network"
	    os.system('python webserver.py')
	    is_connected = 1
	except:
	    pass
	    print "Not connected to the network"
	if time.time() > start + stop_script : break 

# run only the function in this file and not in an import
if __name__ == '__main__':
    is_connected()
