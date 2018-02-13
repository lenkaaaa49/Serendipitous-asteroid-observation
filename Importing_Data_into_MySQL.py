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
import Calculate_Brightness
import Ref_Brightness
from astropy.table import Table
import numpy.ma as ma
from time import gmtime, strftime
import astropy.units as u



def importing_data(password,Obs_date,Special_id1,Vertex1,Vertex2,Vertex3,Vertex4,Instrument,Mode,lambdaMu,eta,pv,relative_reflectance):
    #check if wavelenght is too big
    try:
        for wav1 in lambdaMu:
            if wav1>29.9999:
                raise ValueError("Required wavelenght", wav1,"is too big. Max 29.9999 micron")
    except:
        if lambdaMu>29.9999:
                raise ValueError("Required wavelenght", lambdaMu,"is too big. Max 29.9999 micron")
    # Open database connection
    db = pymysql.connect("localhost","root",password)
    # prepare a cursor object using cursor() method and go to the right database
    cursor = db.cursor()
    cursor.execute("USE ISPY")
    #import url and make a table
    url,z,TYPE=Url_for_ISPY_SkyCoord.ISPY_ephemeris_inSkyCoord('JWST',Obs_date,Special_id1,Vertex1,Vertex2,Vertex3,Vertex4)
    #delete the old data
    sql3 ="DROP TABLE IF EXISTS {0} ".format(Special_id1)
    try:
       # Execute the SQL command
       cursor.execute(sql3)
       # Commit your changes in the database
       db.commit()
    except:
       raise ValueError("Error: unable to delete data in the old table to update it")
    #get table name and create a table for this Specific ID
    table_name,brightness=Setup_Table_in_MySQL_to_Fill_in_Data.makeMySQLtable(Special_id1,password,Obs_date,Vertex1,Vertex2,Vertex3,Vertex4,Instrument,Mode,lambdaMu)
    Special_id=table_name        
    #update the fact that the data has been deleted
    time1=strftime("%Y-%m-%d %H:%M:%S", gmtime())+ ' UTC'
    sql11= "UPDATE INPUT_Table SET Status='NULL',Number_of_Asteroids_Detected=0, Time_Updated_UTC='{0}' where OBS_id='{1}'".format(time1,Special_id)
    try:
        # Execute the SQL command
        cursor.execute(sql11)
        # Commit your changes in the database
        db.commit()
    except:
        # Rollback in case there is any error
        db.rollback()
        raise ValueError("Unable to update the status for OBS_id:"+Special_id+" in the INPUT_Table.")
    
    #check if there are any data on the website
    if z==None:
        #No results
        #update Status in the input table to know if that line has been run already   
        time1=strftime("%Y-%m-%d %H:%M:%S", gmtime())+ ' UTC'
        sql11= "UPDATE INPUT_Table SET Status='UPDATED',Number_of_Asteroids_Detected=0, Time_Updated_UTC='{0}' where OBS_id='{1}'".format(time1,Special_id)
        #print (sql11)
        try:
            # Execute the SQL command
            cursor.execute(sql11)
            # Commit your changes in the database
            db.commit()
        except:
            # Rollback in case there is any error
            db.rollback()
            raise ValueError("Unable to update the status for OBS_id:"+Special_id+"in the INPUT_Table.")
        
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
             'SMAA_3sig', 'SMIA_3sig', 'Theta', 'Pixel_x', 'Pixel_y', 'Last_updated',
             table_name,'OBS_id',Special_id, 'H','G','alpha','r','delta',
             'eta','pv']  
           
           #add Horizons data and the brightness
           asteroid=str(f[x][2]).strip("(")
           asteroid=str(asteroid).strip(")")
           horizons,V=Calculate_Brightness.calculate_brightness(lambdaMu,eta,pv,Obs_date,f[x][2])
          
           #get the reflectance brightness
           reflectance=Ref_Brightness.Reflectance(relative_reflectance,V,lambdaMu)
           
           
           #add brightness values together
           Brightness=[]
           try:
               if horizons[7]==[]:
                   Brightness='empty'
               else:
                   for xx in range(0,len(reflectance)):
                       Brightness.append(horizons[7][xx]+reflectance[xx])

           except: 
               if horizons[7]==[]:
                   Brightness='empty'
               else:
                   Brightness=horizons[7]+reflectance

    
           #input new data
           sql1 = "INSERT INTO {0}(OBS_id,JPL_SPKID,Name_designation,\
                              RA ,\
                              DEC1) \
                   VALUES ('{2}',{1[0]},'{1[2]}','{1[3]}','{1[4]}')".format(tab_col[18],f[x],tab_col[20])

           try:
               # Execute the SQL command
               cursor.execute(sql1)
               # Commit your changes in the database
               db.commit()
           except:
               # Rollback in case there is any error
               db.rollback()
               raise ValueError("Unable to import into table OBS_id:"+Special_id)
           #loop over all the columns in f(add data from ISPY)
           for y in range(0,len(tab_col)-13):
               if y==0 or y==2 or y==3 or y==4:
                    sql1=0
               elif ma.getmask(f[x][y])==True:
                    # Prepare SQL query to INSERT a record into the database.
                    sql1=0
               elif f[x][y]=='NA':
                    # Prepare SQL query to INSERT a record into the database.
                    sql1=0
               else:
                    sql1 = "UPDATE {0} SET {1}='{2}'\
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
                        raise ValueError("Unable to import into table OBS_id:"+Special_id)
           
           #loop over all the columns in horizons  (add data from Horizons and brightness)
           for yy in range(21,28):
                    sql3 = "UPDATE {0} SET {1}='{2}'\
                    where {3}={4}".format(tab_col[18],tab_col[yy],horizons[yy-21],tab_col[0],f[x][0])
                    #print (sql3)
                    try:
                        # Execute the SQL command
                        cursor.execute(sql3)
                        # Commit your changes in the database
                        db.commit()
                    except:
                        # Rollback in case there is any error
                        db.rollback()  
                        raise ValueError("Unable to import into table OBS_id:"+Special_id)
           #print (horizons)             
           try:
                for lam in range(0,len(lambdaMu)):
                    if horizons[7]==[]:
                        sql4="Not possible to calculate brightness"
                    
                    else:
                        #add values for brightness 
                        sql4 = "UPDATE {0} SET `{1}`='{2}'\
                        where {3}={4}".format(tab_col[18],brightness[lam],Brightness[lam],tab_col[0],f[x][0])
                        #print (sql4)
                        try:
                            # Execute the SQL command
                            cursor.execute(sql4)
                            # Commit your changes in the database
                            db.commit()
                        except:
                            # Rollback in case there is any error
                            db.rollback()  
                            raise ValueError("Unable to import into table OBS_id:"+Special_id)
           except:
               if horizons[7]==[]:
                        sql4="Not possible to calculate brightness"
               else:
                    #add values for brightness 
                    sql4 = "UPDATE {0} SET `{1}`='{2}'\
                        where {3}={4}".format(tab_col[18],brightness[0],Brightness,tab_col[0],f[x][0])
                    #print (sql4)
                    try:
                        # Execute the SQL command
                        cursor.execute(sql4)
                        # Commit your changes in the database
                        db.commit()
                    except:
                        # Rollback in case there is any error
                        db.rollback()  
                        raise ValueError("Unable to import into table OBS_id:"+Special_id)

                        
                        
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
               time1=strftime("%Y-%m-%d %H:%M:%S", gmtime())+ ' UTC'
               sql11= "UPDATE INPUT_Table SET Status='UPDATED',Number_of_Asteroids_Detected={1}, Time_Updated_UTC='{2}' where OBS_id='{0}'".format(tab_col[18],result2[0],time1)
               #print (sql11)
               try:
                    # Execute the SQL command
                    cursor.execute(sql11)
                    # Commit your changes in the database
                    db.commit()
               except:
                    # Rollback in case there is any error
                    db.rollback()
                    raise ValueError("Unable to update the status for OBS_id:"+Special_id+"in the INPUT_Table.")
           
           else: 
               print ('For OBS ID ',Special_id,': The number of asteroids in the database is not the same as from ISPY')
       
        except:
           raise ValueError('For OBS ID ',Special_id,": Error: unable to fetch data to check if all the data have been recorded into the database.")
    # disconnect from server
    db.close() 
    return Special_id1