#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 17 15:19:49 2018

@author: lenka
"""

import pymysql

import Url_for_ISPY_SkyCoord
import Create_ISPY_Table
import Setup_Table_in_MySQL_to_Fill_in_Data
from astropy.table import Table
import numpy.ma as ma

def importing_data(password,Obs_date,Special_id1,Vertex1,Vertex2,Vertex3,Vertex4,Instrument,Mode):
    # Open database connection
    db = pymysql.connect("localhost","root",password)
    # prepare a cursor object using cursor() method and go to the right database
    cursor = db.cursor()
    cursor.execute("USE ISPY")
    #import url and make a table
    url,z,TYPE=Url_for_ISPY_SkyCoord.ISPY_ephemeris_inSkyCoord('JWST',Obs_date,Special_id1,Vertex1,Vertex2,Vertex3,Vertex4)
    #get table name and create a table for this Specific ID
    table_name=Setup_Table_in_MySQL_to_Fill_in_Data.makeMySQLtable(Special_id1,password,Obs_date,Vertex1,Vertex2,Vertex3,Vertex4,Instrument,Mode)
    Special_id=table_name
    #delete the old data
    sql3 ="TRUNCATE TABLE {0} ".format(Special_id)
    try:
       # Execute the SQL command
       cursor.execute(sql3)
       # Commit your changes in the database
       db.commit()
    except:
       print ("Error: unable to delete data")
    #check if there are any data on the website
    if z==None:
        #No results
        #update Status in the input table to know if that line has been run already     
        sql11= "UPDATE INPUT_Table SET Status='UPDATED',Number_of_Asteroids_Detected=0, Time_Updated=NOW() where OBS_id='{0}'".format(Special_id)
        #print (sql11)
        try:
            # Execute the SQL command
            cursor.execute(sql11)
            # Commit your changes in the database
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
        
    else:
        #get the table and the tablelines
        distant,tablelines=Create_ISPY_Table.make_table(z,'SPK-ID','EXPLANATION',1,1)
        #make the table into lines to put in the database
        f=Table.as_array(distant)
        
        #make a string of JPL_SPKID values
        JPL_SPKID=[]
        #loop over all the rows in the table from ISPY
               
        for x in range(0,len(f)):
           JPL_SPKID.append(f[x][0])
            
           #table columns
           tab_col=['JPL_SPKID', 'IAU_Number', 'Name_designation','RA', 'DEC1', 'Amag',
                     'dRAcosD', 'dDEC_by_dt', 'CntDst', 'PsAng', 'Data_Arc', 'Nobs', 
                     'Error', 'Ellipse', 'Theta','Pixel_x', 'Pixel_y', 'Last_updated',table_name,'OBS_id',Special_id]
        
            
           #input new data
           sql1 = "INSERT INTO {0}(OBS_id,JPL_SPKID,Name_designation,\
                              RA ,\
                              DEC1 ,Last_Updated)\
                   VALUES ('{2}',{1[0]},'{1[2]}','{1[3]}','{1[4]}',NOW())".format(tab_col[18],f[x],tab_col[20])
           
           try:
               # Execute the SQL command
               cursor.execute(sql1)
               # Commit your changes in the database
               db.commit()
           except:
               # Rollback in case there is any error
               db.rollback()
           #loop over all the columns  
           for y in range(0,len(tab_col)-6):
               if y==0 or y==2 or y==3 or y==4:
                    sql1=0
               elif ma.getmask(f[x][y])==True:
                    # Prepare SQL query to INSERT a record into the database.
                    sql1=0
               else:
                    sql1 = "UPDATE {0} SET {1}={2}\
                    where {3}={4}".format(tab_col[18],tab_col[y],f[x][y],tab_col[0],f[x][0])
                    #print (x,y,f[x][y])
                    try:
                        # Execute the SQL command
                        cursor.execute(sql1)
                        # Commit your changes in the database
                        db.commit()
                    except:
                        # Rollback in case there is any error
                        db.rollback()  
                        
                        
        #check if the number of rows in f and in MySQL is the same (so if all the data has been imported)            
        sql2 = "SELECT COUNT(*) FROM {0}".format(tab_col[18])
        
        try:
           # Execute the SQL command
           cursor.execute(sql2)
           # Fetch all the rows in a list of lists.
           result2 = cursor.fetchone()
           # Now check fetched result
           if result2[0]==len(f):
               print ('For OBS ID ',Special_id,': All the data have been recorded into the database.')
               
               #update Status in the input table to know if that line has been run already     
               sql11= "UPDATE INPUT_Table SET Status='UPDATED',Number_of_Asteroids_Detected={1}, Time_Updated=NOW() where OBS_id='{0}'".format(tab_col[18],result2[0])
               #print (sql11)
               try:
                    # Execute the SQL command
                    cursor.execute(sql11)
                    # Commit your changes in the database
                    db.commit()
               except:
                    # Rollback in case there is any error
                    db.rollback()
           
           else: 
               print ('For OBS ID ',Special_id,': The number of rows in the database is not the same as from ISPY')
       
        except:
           print ('For OBS ID ',Special_id,": Error: unable to fetch data")
    # disconnect from server
    db.close() 
    return Special_id1