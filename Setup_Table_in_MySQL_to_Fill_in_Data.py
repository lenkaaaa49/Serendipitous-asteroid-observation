#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 15:18:20 2017
@author: lenka
"""

import pymysql

#creates a table to put in the data from the website
def makeMySQLtable(table_name,password,user,Obs_date,Vertex1,Vertex2,Vertex3,Vertex4,Instrument,Mode,LambdaMu):
    Special_id=table_name
    
    # Open database connection (host, user, password)
    db = pymysql.connect("localhost","{0}".format(user),"{0}".format(password))
    
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    #use the database
    cursor.execute("USE ISPY")
    
    ## Drop table if it already exist using execute() method.
    #cursor.execute("DROP TABLE IF EXISTS Distant2")
    #table columns
    tab_col=['JPL_SPKID', 'IAU_Number', 'Name_designation','RA', 'DEC1', 'Amag',
             'dRAcosD', 'dDEC_by_dt', 'CntDst', 'PsAng', 'Data_Arc', 'Nobs', 
             'SMAA_3sig', 'SMIA_3sig', 'Theta', 'Pixel_x', 'Pixel_y', 'Last_updated',
             table_name,'OBS_id',Special_id, 'H','G','alpha','r','delta',
             'eta','pv','Relative_reflectance']
    #set up the comemnt for the table
    Obs_date = str(Obs_date).strip().replace(" ", "_")
    Vertex1 = str(Vertex1).strip().replace(" ", "_")
    Vertex2 = str(Vertex2).strip().replace(" ", "_")
    Vertex3 = str(Vertex3).strip().replace(" ", "_")
    Vertex4 = str(Vertex4).strip().replace(" ", "_")
    
    comment=(Obs_date,Instrument,Mode,Vertex1,Vertex2,Vertex3,Vertex4)
    #print (comment)
    
    
    # Create table as per requirement
    sql = "CREATE TABLE IF NOT EXISTS {0}(\
                             {1} VARCHAR(30),\
                             {2} INT NOT NULL PRIMARY KEY,\
                             {3} INT ,\
                             {4} VARCHAR(20) NOT NULL,\
                             {5} VARCHAR(20) NOT NULL,\
                             {6} VARCHAR(20) NOT NULL,\
                             {7} VARCHAR(10),\
                             {8} DEC(5,2),\
                             {9} DEC(5,2),\
                             {10}  DEC(5,1),\
                             {11} DEC(4,1),\
                             {12} VARCHAR(15) ,\
                             {13} INT,\
                             {14} FLOAT,\
                             {15} FLOAT,\
                             {16} DEC(4,1),\
                             {17} VARCHAR(30),\
                             {18} VARCHAR(30),\
                             {19} VARCHAR(30),\
                             {20} VARCHAR(30),\
                             {21} VARCHAR(30),\
                             {22} VARCHAR(30),\
                             {23} VARCHAR(30),\
                             {24} VARCHAR(30),\
                             {25} VARCHAR(30),\
                             {26} VARCHAR(30),\
                             FOREIGN KEY (OBS_id)\
                             REFERENCES INPUT_Table(OBS_id)\
                             ON DELETE CASCADE\
                             ON UPDATE CASCADE)\
                             comment='Obs_date={28},Instrument={29},\
                             Mode={30},FOV={31},{32},{33},{34}'".format(tab_col[18],
                             tab_col[19],tab_col[0],tab_col[1],tab_col[2],
                             tab_col[3],tab_col[4],tab_col[5],
                             tab_col[6],tab_col[7],tab_col[8],tab_col[9],
                             tab_col[10],tab_col[11],tab_col[12],tab_col[13],
                             tab_col[14],tab_col[15],tab_col[16],
                             tab_col[21],tab_col[22],tab_col[23],tab_col[24],
                             tab_col[25],tab_col[26],tab_col[27],tab_col[28],
                             tab_col[27],
                             comment[0],comment[1],comment[2],comment[3],
                             comment[4],comment[5],comment[6])
    try:
        cursor.execute(sql)
    except:
        raise ValueError("Not possible to create a table in MySQL to input data into. Check your command for MySQL.")
   
    
    #make a string of column names for brightness at different wavelenghts
    brightness=[]
    try:
        for lam in range(0,len(LambdaMu)):
            brightness.append('Brightness_'+'{0}'.format(LambdaMu[lam])+'Micron')
            #add the needed number of columns for brightness
            sql1="ALTER TABLE {0} ADD `{1}` VARCHAR(60)".format(tab_col[18],brightness[lam])
            try:
                cursor.execute(sql1)
            except:
                raise ValueError("Not possible to add more columns in MySQL table. Check your Lambda input.")
    except:
        brightness.append('Brightness_'+'{0}'.format(LambdaMu)+'Micron')
        #add the needed number of columns for brightness
        sql1="ALTER TABLE {0} ADD `{1}` VARCHAR(60)".format(tab_col[18],brightness[0])
        try:
            cursor.execute(sql1)
        except:
            raise ValueError("Not possible to add more columns in MySQL table.")


    return table_name,brightness