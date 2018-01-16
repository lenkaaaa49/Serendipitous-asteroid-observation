#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 22 11:45:20 2017

@author: lenka
"""


# coding: utf-8

# make a table from data on a website
# L.Husarova@sron.nl, 27.11.2017
# Partially based on Migo Mueller's script
# which in turn is partially based on a script by Michael Mommert and Alex Hagen


import urllib.request
import urllib.parse
from astropy.table import Table
import urllib.request
import urllib.parse

def call_url(url):
    #url of the website
    #open the website
    f = urllib.request.urlopen(url)
    z=f.read().decode('utf-8')
    #split the data on the website by lines
    riadky=z.split('\n')
     
    #checks if there are data on the website
    for idx,line in enumerate(riadky): #number the lines
        if line.find('No cataloged asteroids were found in the specified field') > -1: 
                
            print ('No cataloged asteroids were found in the specified field.')
            break

        elif line.find('Unexpected Output') > -1: 
             print(line[82:len(line)])
             print('Check your inputs and try again')
        
        elif len(riadky)<=5:
            if line.find('Error') > -1: 
                out=riadky[1].split('<')
                print(out[0])
                break
    
    return z


def make_table(z,beginsymbol,endsymbol,start,end): 

    #beginsymbol-the symbol(word) at the start of the table
    #end symbol-the symbol(word) at the end of the table
    #start-number to specify if the table start at the symbol(start=0) or before(start=positive nuber) or after(negative number)
    #end-number to specify if the table end at the symbol(start=0) or before(start=positive nuber) or after(negative number)
    #datastart-number to specify in which line the data actually starts
    
    
    #split it by lines(riadkov)
    riadky=z.split('\n')
    
    
    # Find interesting output 
    for idx,line in enumerate(riadky): #number the lines
        if line.find(beginsymbol) > -1: #find the beginning line
            FDl=idx-start
            #print ('Beginning',FDl)
            break
    for idx,line in enumerate(riadky): #number the lines
        if line.find(endsymbol) > -1: #find the end line
            lDl=idx-end
            #print ('End',lDl)
            break
    ii=0
    remove=[]
    for idx,line in enumerate(riadky): #number the lines
        if line.find(">....") > -1: #find the limitations, lines which should not be part of the table
            remove.append(idx)
            ii=ii+1

    #substract the number of the beginning line     
    for x in range (0,len(remove)):
        remove[x]=remove[x]-FDl

    
    tablelines=riadky[FDl:lDl] #pick out the table lines
    for z in range (0,len(remove)):
        tablelines.pop(remove[len(remove)-1-z]) #remove limitations
    
    
    #make the table, header is at line 0, data starts at 3rd line, col_start needs to be changed according to the columns required
    Datatable=Table.read(tablelines, guess=False, format='ascii.fixed_width',  delimiter=' ',
                   header_start=0, data_start=3, col_starts=(0,8,15,35,53,66,74,82,91,98,104,114,119,129,139,), 
                     names=('JPL SPK-ID', 'IAU Number', 'Name or designation', 'RA (HH MM SS.ff)', 'DEC (DG MN SC.f)','Amag', 'dRA*cosD ("/hr)','d(DEC)/dt ("/hr)', 'Cnt.Dst (arcsec)', 'PsAng (DEG)','Data Arc (span/#day)','Nobs','Error (SMAA_3sig)','Ellipse (SMIA_3sig)', 'Theta')) 
    #returns the table
    return (Datatable,tablelines)



