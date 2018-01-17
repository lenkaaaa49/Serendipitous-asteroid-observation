#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 15:18:20 2017

@author: lenka
"""

import pymysql

import url_for_ISPY_SkyCoord
import Create_ISPYtable
import Setup_table_inMYSQL_tofillin_data
import Open_InputDatabase
import importingdata_intoMYSQL
from astropy.table import Table
import numpy.ma as ma
from DateTime import Timezones, DateTime
zones = set(Timezones())

#def importDATA(password,Option,Older_than_date):
password='34GH2B.'
Option=2
Older_than_date=DateTime('2018/01/17 15:50:00')
#import input data from MIGO table
Special_id1,Obs_date,Vertex1,Vertex2,Vertex3,Vertex4,Status,Updated_Date=Open_InputDatabase.getinputs(password)
# Open database connection
db = pymysql.connect("localhost","root",password)
# prepare a cursor object using cursor() method and go to the right database
cursor = db.cursor()
cursor.execute("USE ISPY")
count=0

#add new lines (new data)
if Option==1:
    #loop over each special ID
    for ii in range (0,2):#len(Special_id1)):
        if Status[ii]!='UPDATED':
            Special_ID=importingdata_intoMYSQL.importing_data(Option,password,Obs_date[ii],Special_id1[ii],Vertex1[ii],Vertex2[ii],Vertex3[ii],Vertex4[ii])

    if 'NULL' not in Status:
        print('No new data to add')
        
#go over data older than xyDate and update them/add them
elif Option==2:
    #loop over each special ID
    for ii in range (0,2):#len(Special_id1)):
        if Status[ii]=='UPDATED':
            if Updated_Date[ii]<Older_than_date:
                Special_ID=importingdata_intoMYSQL.importing_data(Option,password,Obs_date[ii],Special_id1[ii],Vertex1[ii],Vertex2[ii],Vertex3[ii],Vertex4[ii])
            else:
                count=count+1
                if count==len(Special_id1):
                    print('No outdated tables')
             
#adds new data and updates all the outdated ones    
elif Option==3:
    #loop over each special ID
    for ii in range (0,2):#len(Special_id1)):
        Special_ID=importingdata_intoMYSQL.importing_data(Option,password,Obs_date[ii],Special_id1[ii],Vertex1[ii],Vertex2[ii],Vertex3[ii],Vertex4[ii])

#adds new data and go over data older than xyDate and update them/add them
elif Option==4:
    #loop over each special ID
    for ii in range (0,3):#len(Special_id1)):
        if Updated_Date[ii]<Older_than_date or Status[ii]=='NULL':
            Special_ID=importingdata_intoMYSQL.importing_data(Option,password,Obs_date[ii],Special_id1[ii],Vertex1[ii],Vertex2[ii],Vertex3[ii],Vertex4[ii])
               
else:
    print("Check your inputs")

# disconnect from server
db.close()        
    #return Special_id1