#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 15:18:20 2017

@author: lenka
"""
import pymysql

import Open_Input_Database
import Importing_Data_into_MySQL


def choose_function(password,Option,Older_than_date=None):
    #password='34GH2B.'
    #Option=2
    #Older_than_date=DateTime('2018/01/17 15:50:00')
    Special_id1=[]
    try:
        # Open database connection
        db = pymysql.connect("localhost","root",password)
        # disconnect from server
        db.close() 
        try:
            #import input data from MIGO table
            Special_id1,Obs_date,Vertex1,Vertex2,Vertex3,Vertex4,Status,Updated_Date=Open_Input_Database.getinputs(password)
            count=0
            
            #add new lines (new data)
            if Option==1:
                #loop over each special ID
                for ii in range (0,len(Special_id1)):
                    if Status[ii]!='UPDATED':
                        Special_ID=Importing_Data_into_MySQL.importing_data(Option,password,Obs_date[ii],Special_id1[ii],Vertex1[ii],Vertex2[ii],Vertex3[ii],Vertex4[ii])
            
                if 'NULL' not in Status:
                    print('No new data to add')
                    
            #go over data older than xyDate and update them/add them
            elif Option==2:
                if Older_than_date==None:
                    print ('Check your inputs (date)') 
                else:
                    #loop over each special ID
                    for ii in range (0,len(Special_id1)):
                        if Status[ii]=='UPDATED':
                            if Updated_Date[ii]<Older_than_date:
                                Special_ID=Importing_Data_into_MySQL.importing_data(Option,password,Obs_date[ii],Special_id1[ii],Vertex1[ii],Vertex2[ii],Vertex3[ii],Vertex4[ii])
                            else:
                                count=count+1
                                if count==len(Special_id1):
                                    print('No outdated tables')
                         
            #adds new data and updates all the outdated ones    
            elif Option==3:
                #loop over each special ID
                for ii in range (0,len(Special_id1)):
                    Special_ID=Importing_Data_into_MySQL.importing_data(Option,password,Obs_date[ii],Special_id1[ii],Vertex1[ii],Vertex2[ii],Vertex3[ii],Vertex4[ii])
                if 'NULL' not in Status:
                    print('No new data to add')
                    
            #adds new data and go over data older than xyDate and update them/add them
            elif Option==4:
                if Older_than_date==None:
                    print ('Check your inputs (date)')
                else:
                    #loop over each special ID
                    for ii in range (0,len(Special_id1)):
                        if Updated_Date[ii]<Older_than_date or Status[ii]=='NULL':
                            Special_ID=Importing_Data_into_MySQL.importing_data(Option,password,Obs_date[ii],Special_id1[ii],Vertex1[ii],Vertex2[ii],Vertex3[ii],Vertex4[ii])
                        else:
                            count=count+1
                            if count==len(Special_id1):
                                print('No outdated tables and no new data to add')
                    if 'NULL' not in Status and count!=len(Special_id1):
                        print('No new data to add')      
                        
            else:
                print("Check your inputs (Option)")
        except:
            print ('Something went wrong')
    except:
        print ('Check your inputs (password)')
      
    return Special_id1