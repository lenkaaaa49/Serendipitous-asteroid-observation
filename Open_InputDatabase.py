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
       print ("Error: unable to fetch data")
    
    #save up data to specific strings, and change the class(Skycoord,Datetime,Quantity)
    Special_id=[]
    Obs_date=[]
    Vertex1=[]
    Vertex2=[]
    Vertex3=[]
    Vertex4=[]
    #depending on which data are in the tables
    for x in range(0,len(result)):   
        Special_id.append(result[x][0])
        Obs_date.append(DateTime(result[x][1]))
        Vertex1.append(SkyCoord(result[x][3],result[x][4]))
        if result[x][6]==None:
            Vertex2.append(u.Quantity(result[x][5]))
            if result [x][7]==None:
                Vertex3.append(None)
                Vertex4.append(None)
            else:
                Vertex3.append(u.Quantity(result[x][7]))
                Vertex4.append(u.Quantity(result[x][9]))
        else:
            Vertex2.append(SkyCoord(result[x][5],result[x][6]))
            Vertex3.append(SkyCoord(result[x][7],result[x][8]))
            Vertex4.append(SkyCoord(result[x][9],result[x][10]))
    
    # disconnect from server
    db.close()
    
    return Special_id,Obs_date,Vertex1,Vertex2,Vertex3,Vertex4