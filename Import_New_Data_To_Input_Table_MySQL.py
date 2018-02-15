#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 13:43:53 2018

@author: lenka
"""

import pymysql
import Read_Input_Files

def Import_new_data_into_input_table(Login_Input,Add_data):
    #get data from the input files 
    user,password=Read_Input_Files.Get_user_password(Login_Input)
    
    f = open(Add_data, 'r')
        
    #look for the user name and password
    for idx,line in enumerate(f.readlines()): #number the lines
            if idx>0 and line!='\n':
                
                data=line.split(',')
                
                # Open database connection
                db = pymysql.connect("localhost","{0}".format(user),"{0}".format(password))
                # prepare a cursor object using cursor() method and go to the right database
                cursor = db.cursor()
                cursor.execute("USE ISPY")
            
                #add new data
                sql1= "INSERT INTO INPUT_Table (`OBS_id`,`Observation_date`,`Instrument`,`Mode`,`Vertex1_1`,`Vertex1_2`,`Vertex2_1`,`Vertex2_2`,`Vertex3_1`,`Vertex3_2`,`Vertex4_1`,`Vertex4_2`) \
                VALUES ('{0[0]}','{0[1]}','{0[2]}','{0[3]}','{0[4]}','{0[5]}','{0[6]}','{0[7]}','{0[8]}','{0[9]}','{0[10]}','{0[11]}')".format(data)
                print (sql1)
                
                try:
                    # Execute the SQL command
                    cursor.execute(sql1)
                    # Commit your changes in the database
                    db.commit()
                except:
                    # Rollback in case there is any error
                    db.rollback()
                    print ("Error importing data into the table")
            
    
    # disconnect from server
    db.close()

    return
