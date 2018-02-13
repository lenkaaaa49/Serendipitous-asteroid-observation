#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 11:49:49 2018

@author: lenka
"""

import callhorizons
import pandas as pd
import astropy.units as u
import neatm

def calculate_brightness(lambdaMu,eta,pv,obs_date,asteroid):
    
    #convert the date in Julian days
    dt = pd.DatetimeIndex(['{0}'.format(obs_date)], dtype='datetime64[ns]', name=u'date', freq=None)
    j = dt.to_julian_date()
    
    #call horizons and get the needed data to calculate brightness
    eros = callhorizons.query('{0}'.format(asteroid))
    eros.set_discreteepochs([j[0]])
    eros.get_ephemerides('@JWST')
    
    #get website link
    #print (eros.query)
    
    try:
        #make a string with all the data
        alldata=[eros['H'][0], eros['G'][0],eros['alpha'][0],eros['r'][0],eros['delta'][0],eta,pv]
        V=eros['V'][0]
    except:
        raise ValueError("Cannot get values from Horizons")

    
    result=[]   
    try:
        try:
            for wav in lambdaMu:
                #use Neatm function to calculate the brightness
                result1=neatm.neatm(alldata[0],alldata[1],alldata[2]*u.deg,alldata[3]*u.AU,alldata[4]*u.AU,wav*u.micron,eta,pv)
                result.append(result1)
        except:
            wav=lambdaMu
            #use Neatm function to calculate the brightness
            result=neatm.neatm(alldata[0],alldata[1],alldata[2]*u.deg,alldata[3]*u.AU,alldata[4]*u.AU,wav*u.micron,eta,pv)
            
    except:
        result=[] 
      
    alldata.append(result)
    return alldata,V

