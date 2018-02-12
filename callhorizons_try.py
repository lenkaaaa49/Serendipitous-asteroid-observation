#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 11:49:49 2018

@author: lenka
"""

import callhorizons
import pandas as pd
from astropy.coordinates import SkyCoord
from astropy.coordinates import ICRS, Galactic, FK4, FK5  # Low-level frames
from astropy.coordinates import Angle, Latitude, Longitude  # Angles
import astropy.units as u
import neatm

#def calculate_brightness(lambdaMu,eta,pv,obs_date,asteroid):
lambdaMu=10
eta=1.3
pv=0.2
    
dt = pd.DatetimeIndex(['2017/03/09 13:45:00 UTC'], dtype='datetime64[ns]', name=u'date', freq=None)
j = dt.to_julian_date()
print(j)

eros = callhorizons.query('34708')
eros.set_discreteepochs([j[0]])
eros.get_ephemerides('@JWST')
alldata=eros.get_elements()

#print(eros['RA'], eros['DEC'],eros['G'],eros['H'],eros['r'],eros['alpha'])
#check if the SkyCoord is right
#l=SkyCoord('01:27:18.71 +25 39 02.2', unit=(u.hour, u.deg))
#print (l)

result=neatm.neatm(eros['H'][0],eros['G'][0],eros['alpha'][0]*u.deg,eros['r'][0]*u.AU,eros['delta'][0]*u.AU,lambdaMu*u.micron,eta,pv)
print (result)

#return result,alldata
