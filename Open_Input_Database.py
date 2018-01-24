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
        for x in range(0,len(result)):   
            Special_id.append(result[x][0])
            Obs_date.append(DateTime(result[x][1]))
            Instrument.append(result[x][2])
            Mode.append(result[x][3])
            Status.append(result[x][12])
            Updated_Date.append(DateTime(result[x][14]))
            Vertex1.append(SkyCoord(result[x][4],result[x][5]))
            if result[x][7]==None:
                Vertex2.append(u.Quantity(result[x][6]))
                if result [x][8]==None:
                    Vertex3.append(None)
                    Vertex4.append(None)
                else:
                    Vertex3.append(u.Quantity(result[x][8]))
                    Vertex4.append(u.Quantity(result[x][10]))
            else:
                Vertex2.append(SkyCoord(result[x][6],result[x][7]))
                Vertex3.append(SkyCoord(result[x][8],result[x][9]))
                Vertex4.append(SkyCoord(result[x][10],result[x][11]))
    except:
        raise ValueError('Error: Check the data in the INPUT_Table')
    #print (Status, Updated_Date)
    # disconnect from server
    db.close()
    
    return Special_id,Obs_date,Vertex1,Vertex2,Vertex3,Vertex4,Status,Updated_Date,Instrument,Mode