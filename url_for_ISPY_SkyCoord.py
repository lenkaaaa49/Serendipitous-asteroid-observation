#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 29 16:33:42 2017

@author: lenka
"""

import urllib
import Check_for_Connection
from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.coordinates import ICRS, Galactic, FK4, FK5  
from DateTime import Timezones, DateTime
zones = set(Timezones())

# See https://ssd.jpl.nasa.gov/x/ispy.html
# ftp://ssd.jpl.nasa.gov/pub/ssd/ispy_mail_example.long (Documentation)


## Certex1--4 can all be SkyCoord's; in that case the function searches the polygon spanned by them
## Vertex1 can be FOV center, vertex2 an astropy angle; in that case the function searches the circle with that radius
## Vertex1 can be FOV center, then vertex2--4 are astopy angles, in that case function searches a rectangle
def ISPY_ephemeris_inSkyCoord(IDnumber, date, Special_id, Vertex1=None, Vertex2=None, Vertex3=None, Vertex4=None):
    
    #IDnumber of the body-center (JWST -170, Spitzer= -79, HERSCHEL= -486, WISE= -163, ISO= -64,
    #Rosetta= -226, Chandra= -151, STEREO-A= -234, STEREO-B= -235, Earth geocentric= 399, Mars center= 499)
    #date: day of the obseravtion in UTC time, input in DateTime, can be in different time zones
    
    #the field-of-view can be specified (in this file): 1= Polygon   (RA/DEC corners of four vertices) 
                                                    #2= Circle    (center & radius)
                                                    #3= Rectangle (center & RA_width & DEC_width & CCW_angle)
   
    #RA, DEC: of the rectangular field' central point. The coordinate should be in the J2000 equatorial coordinate system. 
    #for the following the input can be with units, if not specified, the units are assumed to be as specified below
    #RAW: Right Ascension direction, in units of arcseconds
    #DCW: Declination direction, in units of arcseconds
    #PHI: rotation angle of the rectangular field in units of degrees, relative to Celestial North (a line of constant RA, for example).
        #Counter-clockwise rotation angles are positive. Clockwise rotation angles are negative.
    #RADIUS: radius of the circle, in arcsec
  
    
    # prepare date
    if isinstance(date,DateTime) is True:
        date= date.toZone('UTC')
        date = str(date.ISO()).strip().replace(" ", "%20") 
    else:
        print ('Check your date input')
    
        
    #prepare IDnumber
    dict = {'JWST': '-170', 'Spitzer': '-79', 'HERSCHEL': '-486', 'WISE':'-163','ISO':'-64','Rosetta':'-226', 'Chandra':'-151','STEREO A':'-234','STEREO B':'-235','Earth':'399','Mars':'499'}
    if IDnumber in dict.keys():
        IDnumber=dict[IDnumber]
    elif IDnumber in dict.values():
        IDnumber=IDnumber
    else: 
        print ('Check your observer')
    
    # prepare URL
    url= None
     
    #check which kind of field of view it is, and depending on that make a url
    if isinstance(Vertex1,SkyCoord) is True and isinstance(Vertex2,SkyCoord) is True and isinstance(Vertex3,SkyCoord) is True and isinstance(Vertex4,SkyCoord) is True:
        TYPE='1'
        TYPE1='Polygon'
        
        #add parts to the url
        url = "https://ssd.jpl.nasa.gov/cgi-bin/ispy.cgi?"
        url += "SPKID=%27"+str(IDnumber)
        url += "%27&FOV_DATE=%27"+str(date)
        url += "%27&TYPE=%27"+str(TYPE) 
        
        #convert RA and DEC to ICRS coordinate system
        Vertex1=Vertex1.transform_to(ICRS)
        Vertex1=Vertex1.transform_to(ICRS)
        Vertex1=Vertex1.transform_to(ICRS)
        Vertex1=Vertex1.transform_to(ICRS)
        
        url += "%27&RA(1)=%27"+str(Vertex1.ra.deg)
        url += "%27&DEC(1)=%27"+str(Vertex1.dec.deg)
        url += "%27&RA(2)=%27"+str(Vertex2.ra.deg)
        url += "%27&DEC(2)=%27"+str(Vertex2.dec.deg)
        url += "%27&RA(3)=%27"+str(Vertex3.ra.deg)
        url += "%27&DEC(3)=%27"+str(Vertex3.dec.deg)
        url += "%27&RA(4)=%27"+str(Vertex4.ra.deg)
        url += "%27&DEC(4)=%27"+str(Vertex4.dec.deg)
        
    elif isinstance(Vertex1,SkyCoord) is True and isinstance(Vertex2,u.Quantity) is True and Vertex3==None and Vertex4==None:
        TYPE='2'
        TYPE1='Circle'
        
        #convert RA and DEC to ICRS coordinate system
        Vertex1=Vertex1.transform_to(ICRS)
        
        #convert radius to arcsec
        RADIUS=Vertex2.to(u.arcsec)
        RADIUS='{0.value}'.format(RADIUS)
        
        url = "https://ssd.jpl.nasa.gov/cgi-bin/ispy.cgi?"
        url += "SPKID=%27"+str(IDnumber)
        url += "%27&FOV_DATE=%27"+str(date)
        url += "%27&TYPE=%27"+str(TYPE)

        url += "%27&RA(1)=%27"+str(Vertex1.ra.deg)
        url += "%27&DEC(1)=%27"+str(Vertex1.dec.deg)
        url += "&RADIUS=%27"+str(RADIUS)
        
    
    elif isinstance(Vertex1,SkyCoord) is True and isinstance(Vertex2,u.Quantity) is True and isinstance(Vertex3,u.Quantity) is True and isinstance(Vertex4,u.Quantity) is True:
        TYPE='3'
        TYPE1='Rectangle'
        
        #convert RA and DEC to ICRS coordinate system
        Vertex1=Vertex1.transform_to(ICRS)
        
        #convert other quatities to the needed units
        RAW=Vertex2.to(u.arcsec)
        RAW='{0.value}'.format(RAW)
        DCW=Vertex3.to(u.arcsec)
        DCW='{0.value}'.format(DCW)
        PHI=Vertex4.to(u.deg) 
        PHI='{0.value}'.format(PHI)
                
        url = "https://ssd.jpl.nasa.gov/cgi-bin/ispy.cgi?"
        url += "SPKID=%27"+str(IDnumber)
        url += "%27&FOV_DATE=%27"+str(date)
        url += "%27&TYPE=%27"+str(TYPE) 
        
        url += "%27&RA(1)=%27"+str(Vertex1.ra.deg)
        url += "%27&DEC(1)=%27"+str(Vertex1.dec.deg)
        url += "&RAW=%27"+str(RAW)
        url += "&DCW=%27"+str(DCW)
        url += "&PHI=%27"+str(PHI)
        #print (url)
        
    else:
        print ('Check your inputs')
    
    #check if the internet works
    loop=Check_for_Connection.check_connection()
    
    #url-website
    #open the website
    f = urllib.request.urlopen(url)
    z=f.read().decode('utf-8')
    
        
    riadky=z.split('\n')
    
    #check if the website has any data, or if there is an error
    for idx,line in enumerate(riadky): #number the lines
        if line.find('No cataloged asteroids were found in the specified field') > -1: #find the beginning line
            z=None    
            print ('For Special ID ',Special_id,': No cataloged asteroids were found in the specified field.')
            break
            

        elif line.find('Unexpected Output') > -1: #find the beginning line
             print(line[82:len(line)])
             print('For Special ID ',Special_id,': Check your inputs and try again')
             z=None
        
        elif len(riadky)<=5:
            if line.find('Error') > -1: 
                out=riadky[1].split('<')
                print('For Special ID ',Special_id,out[0])
                z=None
                break
                
    print ('Url for',Special_id,':',url)      
    return url,z,TYPE1