#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 15:18:20 2017

@author: lenka
"""
import pymysql

import Open_Input_Database
import Importing_Data_into_MySQL


def create_new_tables(password):
#add new lines (new data) in the database
    Special_id1=[]
    try:
        # Open database connection
        db = pymysql.connect("localhost","root",password)
        # disconnect from server
        db.close() 
        try:
            #import input data from MIGO table
            Special_id1,Obs_date,Vertex1,Vertex2,Vertex3,Vertex4,Status,Updated_Date,Instrument,Mode=Open_Input_Database.getinputs(password)

            #loop over each special ID
            for ii in range (0,len(Special_id1)):
                if Status[ii]!='UPDATED':
                    Special_ID=Importing_Data_into_MySQL.importing_data(password,Obs_date[ii],Special_id1[ii],Vertex1[ii],Vertex2[ii],Vertex3[ii],Vertex4[ii],Instrument[ii],Mode[ii])
        
            if 'NULL' not in Status:
                print('No new data to add')
        except:
            print ('Something went wrong')
    except:
        print ('Check your inputs (password)')
    return Special_id1
                    
def update_old_tables(password,Older_than_date):
#go over data older than xyDate and update them/add them
    Special_id1=[]
    try:
        # Open database connection
        db = pymysql.connect("localhost","root",password)
        # disconnect from server
        db.close() 
        try:
            #import input data from MIGO table
            Special_id1,Obs_date,Vertex1,Vertex2,Vertex3,Vertex4,Status,Updated_Date,Instrument,Mode=Open_Input_Database.getinputs(password)
            count=0
            
            if Older_than_date==None:
                print ('Check your inputs (date)') 
            else:
                #loop over each special ID
                for ii in range (0,len(Special_id1)):
                    if Status[ii]=='UPDATED':
                        if Updated_Date[ii]<Older_than_date:
                            Special_ID=Importing_Data_into_MySQL.importing_data(password,Obs_date[ii],Special_id1[ii],Vertex1[ii],Vertex2[ii],Vertex3[ii],Vertex4[ii],Instrument[ii],Mode[ii])
                        else:
                            count=count+1
                            if count==len(Special_id1):
                                print('No outdated tables')
        except:
            print ('Something went wrong')
    except:
        print ('Check your inputs (password)')
      
    return Special_id1            
            
def add_and_update_tables(password):
#adds new data and updates all the outdated ones 
    Special_id1=[]
    try:
        # Open database connection
        db = pymysql.connect("localhost","root",password)
        # disconnect from server
        db.close() 
        try:
            #import input data from MIGO table
            Special_id1,Obs_date,Vertex1,Vertex2,Vertex3,Vertex4,Status,Updated_Date,Instrument,Mode=Open_Input_Database.getinputs(password)

            #loop over each special ID
            for ii in range (0,len(Special_id1)):
                Special_ID=Importing_Data_into_MySQL.importing_data(password,Obs_date[ii],Special_id1[ii],Vertex1[ii],Vertex2[ii],Vertex3[ii],Vertex4[ii],Instrument[ii],Mode[ii])
            if 'NULL' not in Status:
                print('No new data to add')
                    
        except:
            print ('Something went wrong')
    except:
        print ('Check your inputs (password)')
      
    return Special_id1
                    
def add_and_update_tables_after_date(password,Older_than_date):     
#adds new data and go over data older than xyDate and update them/add them
    Special_id1=[]
    try:
        # Open database connection
        db = pymysql.connect("localhost","root",password)
        # disconnect from server
        db.close() 
        try:
            #import input data from MIGO table
            Special_id1,Obs_date,Vertex1,Vertex2,Vertex3,Vertex4,Status,Updated_Date,Instrument,Mode=Open_Input_Database.getinputs(password)
            count=0
            
            if Older_than_date==None:
                print ('Check your inputs (date)')
            else:
                #loop over each special ID
                for ii in range (0,len(Special_id1)):
                    if Updated_Date[ii]<Older_than_date or Status[ii]=='NULL':
                        Special_ID=Importing_Data_into_MySQL.importing_data(password,Obs_date[ii],Special_id1[ii],Vertex1[ii],Vertex2[ii],Vertex3[ii],Vertex4[ii],Instrument[ii],Mode[ii])
                    else:
                        count=count+1
                        if count==len(Special_id1):
                            print('No outdated tables and no new data to add')
                if 'NULL' not in Status and count!=len(Special_id1):
                    print('No new data to add')      
                        
        except:
            print ('Something went wrong')
    except:
        print ('Check your inputs (password)')
      
    return Special_id1