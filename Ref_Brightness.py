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
import astropy.units as u

def Reflectance(relative_reflectance,V,wav):
    #wav=[10,20,25] #micron
    #relative_reflectance=1.4
    #V=2.3
        
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
        wavelenght.append((float(solar_flux_density[x][0])))#/299792458)*10**(29)) #mJy
        solar_flux.append(float(solar_flux_density[x][1]))
    
    #interpolate the values
    s = interpolate.InterpolatedUnivariateSpline(wavelenght, solar_flux)
    xnew = np.arange(0.1998,30,0.0001)
    ynew = s(xnew)
    
    #plot the difference in interpolated and from table
    #    plt.figure()
    #    plt.plot(wavelenght, solar_flux, 'x', xnew, ynew,'b')
    #    plt.legend(['Linear', 'InterpolatedUnivariateSpline'])
    #    plt.title('InterpolatedUnivariateSpline')
    #    plt.show()  
    
    V_sun=[]
    reflectance=[]
    try:
        try:
             for xx in range(0,len(wav)):
                 #find the value of solar flux density wanted at a specified micron value
                 wavelenght_wanted=np.where(xnew.astype('float32') == wav[xx])
                 V_sun.append(ynew[wavelenght_wanted[0][0]])
                 
                 #calculate the reflectence
                 reflectance.append(relative_reflectance*V_sun[xx]*10**(-(V+26.74)/2.5))
               
        except:
             #find the value of solar flux density wanted at a specified micron value
             wavelenght_wanted=np.where(xnew.astype('float32') == wav)
             V_sun=ynew[wavelenght_wanted[0][0]]
             V_sun=5.54e16
             #calculate the reflectence
             reflectance=relative_reflectance*V_sun*10**(-(V+26.74)/2.5)
    except:
        reflectance=[]
        
    return reflectance

