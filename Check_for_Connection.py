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
    while loop_value < 50000:
        #print ("test 2")
        try:
            urllib.request.urlopen("http://google.com")
            loop_value=50000+1
            print( "Network is running" )
        except urllib.error.URLError as e:
            #print("Network currently down")
            loop_value=loop_value+1
            raise ValueError("There appears to be no network connection")
    
    return loop_value