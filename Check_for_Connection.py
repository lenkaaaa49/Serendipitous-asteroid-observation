#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 12:36:17 2018

@author: lenka
"""
import urllib

def check_connection():
    #print ("test 1")
    loop_value = 1
    while loop_value == 1:
        #print ("test 2")
        try:
            urllib.request.urlopen("http://google.com")
            loop_value=0
        except urllib.error.URLError as e:
            print("Network currently down")
    else:
        print( "Network is running" )
    return loop_value