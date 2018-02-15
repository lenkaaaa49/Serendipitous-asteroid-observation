#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  8 16:36:29 2018

@author: lenka
"""
import numpy as np
from astropy.table import Table
import matplotlib.pyplot as plt
from scipy import interpolate
import callhorizons
import pandas as pd
import astropy.units as u


def Reflectance(relative_reflectance,V,wav):
    
    #read the table of the values
    solar_flux_density=Table.read('Rieke2008.fluxSunVega.txt', guess=False,format='ascii.fixed_width',  delimiter=' ',
                   header_start=None, data_start=13,
                   col_starts=(0, 8, 17),
                  col_ends=(7, 16, 26),names=('Wavelength[micron]','Flux density of the Sun[W/m2/nm]',
                        'Flux density of Vega[W/m2/nm]'))
    #make arrayes of wavelenghts and solar flux densities
    wavelenght=[]
    solar_flux=[]
    for x in range(1,len(solar_flux_density)):
        wavelenght.append((float(solar_flux_density[x][0])))
        solar_flux.append(float(solar_flux_density[x][1]))
    
    #interpolate the values
    s = interpolate.InterpolatedUnivariateSpline(wavelenght, solar_flux)
    
    V_sun=[]
    reflectance=[]
    try:
        try:
             for xx in range(0,len(wav)):
                 #find the value of solar flux density wanted at a specified micron value
                 xnew = wav[xx]
                 ynew = s(xnew)
                 #convert to mJy
                 V_sun.append((ynew*u.W/u.m**2/u.nm).to(u.mJy, equivalencies=u.spectral_density(wav[xx] * u.micron)))
                 #calculate the reflectence
                 reflectance.append(relative_reflectance*V_sun[xx]*10**(-(V+26.74)/2.5))
                 #print ('ref', reflectance)
        except:
             #find the value of solar flux density wanted at a specified micron value
             xnew = wav
             ynew = s(xnew)
             #convert to mJy
             V_sun=(ynew*u.W/u.m**2/u.nm).to(u.mJy, equivalencies=u.spectral_density(wav* u.micron))
             
             #calculate the reflectence
             reflectance=relative_reflectance*V_sun*10**(-(V+26.74)/2.5)
    except:
        reflectance=[] 
        
        
    return reflectance

