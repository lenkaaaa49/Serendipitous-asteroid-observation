#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 15:18:20 2017

@author: lenka
"""

import pymysql

#creates a table to put in the data from the website
def makeMySQLtable(table_name,password):
    Special_id=table_name
    
    # Open database connection (host, user, password)
    db = pymysql.connect("localhost","root",password )
    
    # prepare a cursor object using cursor() method
    cursor = db.cursor()
    #create a database ISPY, if there isnt one like that already
    cursor.execute("CREATE DATABASE IF NOT EXISTS ISPY") 
    #use the database
    cursor.execute("USE ISPY")
    
    ## Drop table if it already exist using execute() method.
    #cursor.execute("DROP TABLE IF EXISTS Distant2")
    #table columns
    tab_col=['JPL_SPKID', 'IAU_Number', 'Name_designation','RA', 'DEC1', 'Amag',
             'dRAcosD', 'dDEC_by_dt', 'CntDst', 'PsAng', 'Data_Arc', 'Nobs', 
             'Error', 'Ellipse', 'Theta', 'Last_updated',table_name,'Special_id',Special_id]
    
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
                             {17} TIMESTAMP,\
                             FOREIGN KEY (Special_id)\
                             REFERENCES MIGO_INP(Special_id)\
                             ON DELETE CASCADE\
                             ON UPDATE CASCADE)".format(tab_col[16],tab_col[17],tab_col[0],
                             tab_col[1],tab_col[2],tab_col[3],tab_col[4],tab_col[5],
                             tab_col[6],tab_col[7],tab_col[8],tab_col[9],
                             tab_col[10],tab_col[11],tab_col[12],tab_col[13],
                             tab_col[14],tab_col[15])
    
    cursor.execute(sql)
    
    # disconnect from server
    db.close()
    return table_name