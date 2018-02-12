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
#lambdaMu=10
#eta=1.3
#pv=0.2
    
    #convert the date in Julian days
    dt = pd.DatetimeIndex(['{0}'.format(obs_date)], dtype='datetime64[ns]', name=u'date', freq=None)
    j = dt.to_julian_date()
    #print(j)
    
    #call horizons and get the needed data to calculate brightness
    eros = callhorizons.query('{0}'.format(asteroid))
    eros.set_discreteepochs([j[0]])
    eros.get_ephemerides('@JWST')
    
    #print (eros.query)
    
    try:
        #make a string with all the data
        alldata=[eros['H'][0], eros['G'][0],eros['alpha'][0],eros['r'][0],eros['delta'][0],eta,pv]
        V=eros['V'][0]
    except:
        raise ValueError("Cannot get values from Horizons")
    
    #check if the SkyCoord is right
    #l=SkyCoord('01:27:18.71 +25 39 02.2', unit=(u.hour, u.deg))
    #print (l)
    
    result=[]   
    try:
        try:
            for wav in lambdaMu:
                #use Migo's function to calculate the brightness
                result1=neatm.neatm(alldata[0],alldata[1],alldata[2]*u.deg,alldata[3]*u.AU,alldata[4]*u.AU,wav*u.micron,eta,pv)
                result.append(result1)
        except:
            wav=lambdaMu
            #use Migo's function to calculate the brightness
            result=neatm.neatm(alldata[0],alldata[1],alldata[2]*u.deg,alldata[3]*u.AU,alldata[4]*u.AU,wav*u.micron,eta,pv)
            
    except:
        result=[] 
        
    #print (result)
    alldata.append(result)
    #print(alldata[7][0])

    return alldata,V

