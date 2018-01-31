#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 15:18:20 2017

@author: lenka
"""

import pymysql
from astropy import units as u
from astropy.coordinates import SkyCoord
from astropy.coordinates import ICRS, Galactic, FK4, FK5  
from DateTime import Timezones, DateTime
zones = set(Timezones())
#could put inputs such as the database name and the Migo input table
def getinputs(password): 
    # Open database connection
    db = pymysql.connect("localhost","root",password )
    
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    cursor.execute("USE ISPY")
    
    # Create table as per requirement
    sql = "SELECT * from INPUT_Table"
    try:
       # Execute the SQL command
       cursor.execute(sql)
       #Fetch all the rows in a list of lists.
       result = cursor.fetchall()
    except:
       #print ("Error: unable to fetch data")
       raise ValueError("Error: unable to fetch data from INPUT_Table")
    
    #save up data to specific strings, and change the class(Skycoord,Datetime,Quantity)
    Special_id=[]
    Obs_date=[]
    Instrument=[]
    Mode=[]
    Updated_Date=[]
    Status=[]
    Vertex1=[]
    Vertex2=[]
    Vertex3=[]
    Vertex4=[]
    try:
        
        #depending on which data are in the tables
        for line in result:   
            Special_id.append(line[0])
            Obs_date.append(DateTime(line[1]))
            Instrument.append(line[2])
            Mode.append(line[3])
            Status.append(line[12])
            Updated_Date.append(DateTime(line[14]))
            Vertex1.append(SkyCoord(line[4],line[5]))
            if line[7]==None:
                Vertex2.append(u.Quantity(line[6]))
                if line[8]==None:
                    Vertex3.append(None)
                    Vertex4.append(None)
                else:
                    Vertex3.append(u.Quantity(line[8]))
                    Vertex4.append(u.Quantity(line[10]))
            else:
                Vertex2.append(SkyCoord(line[6],line[7]))
                Vertex3.append(SkyCoord(line[8],line[9]))
                Vertex4.append(SkyCoord(line[10],line[11]))
    except:
        raise ValueError('Error: Check the data in the INPUT_Table. Offending line:'+str(line))
    #print (Status, Updated_Date)
    # disconnect from server
    db.close()
        
    return Special_id,Obs_date,Vertex1,Vertex2,Vertex3,Vertex4,Status,Updated_Date,Instrument,Mode