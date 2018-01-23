#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jan 23 14:36:47 2018

@author: lenka
"""

import os

filename="Idontexist.txt"
try:
    #assert False
    raise ValueError("Unspecified error")
    if not os.path.isfile(filename):
        raise ValueError("File "+filename+" does not exist")
except ValueError as e:
    #print (e)
    text=e.__str__()
    if "does not exist" in text:
        print ("File I/O problem")
    else:
        print ("Some other problem")
        raise
    print ("Never mind, keep going")
    #raise
except Exception as e:
    print ("Something else went wrong, stop")
    print (e)
    print (e.__class__)
    raise
    
print ("Will only get here if everything is fine or ValueError")


#print (ValueError.__istype__(Exception))