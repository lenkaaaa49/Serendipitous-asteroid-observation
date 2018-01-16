#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 15:18:20 2017

@author: lenka
"""

import pymysql

import url_for_ISPY_SkyCoord
import Create_ISPYtable
import Setup_table_inMYSQL_tofillin_data
import Open_InputDatabase
from astropy.table import Table
import numpy.ma as ma

def importDATA(password):
    #import input data from MIGO table
    Special_id1,Obs_date,Vertex1,Vertex2,Vertex3,Vertex4=Open_InputDatabase.getinputs(password)
    Table_NAMES=[]
    #loop over each special ID
    for x in range (0,1):#len(Special_id1)):
        #import url and make a table
        url,z,TYPE=url_for_ISPY_SkyCoord.ISPY_ephemeris_inSkyCoord('JWST',Obs_date[x],Special_id1[x],Vertex1[x],Vertex2[x],Vertex3[x],Vertex4[x])
        #get table name and create a table for this Specific ID
        table_name=Setup_table_inMYSQL_tofillin_data.makeMySQLtable(Special_id1[x],password)
        Special_id=table_name
        #check if there are any data on the website
        if z==None:
            k='No results'
        else:
            #get the table and the tablelines
            distant,tablelines=Create_ISPYtable.make_table(z,'SPK-ID','EXPLANATION',1,1)
            #make the table into lines to put in the database
            f=Table.as_array(distant)
            
            #make a string of JPL_SPKID values
            JPL_SPKID=[]
            for x in range(0,len(f)):
               JPL_SPKID.append(f[x][0])
            
            # Open database connection
            db = pymysql.connect("localhost","root",password)
            
            # prepare a cursor object using cursor() method and go to the right database
            cursor = db.cursor()
            cursor.execute("USE ISPY")
            
            #table columns
            tab_col=['JPL_SPKID', 'IAU_Number', 'Name_designation','RA', 'DEC1', 'Amag',
                     'dRAcosD', 'dDEC_by_dt', 'CntDst', 'PsAng', 'Data_Arc', 'Nobs', 
                     'Error', 'Ellipse', 'Theta', 'Last_updated',table_name,'Special_id',Special_id]
            
            #check if there are any data in the table already
            sql3 ="SELECT {0} from {1}".format(tab_col[0],tab_col[16])
            try:
               # Execute the SQL command
               cursor.execute(sql3)
               #Fetch all the rows in a list of lists. These are the data which are already in the database
               result = cursor.fetchall()
            except:
               print ("Error: unable to fetch data")
                        
            #select the data from the table which are older than 1 month       
            sql4 ="SELECT {0} from {1} where {2}<NOW()-INTERVAL 1 MONTH".format(tab_col[0],tab_col[16],tab_col[15])
            try:
               # Execute the SQL command
               cursor.execute(sql4)
               # Fetch all the rows in a list of lists. these are the data which are older than 1 month
               result1 = cursor.fetchall()
               # Now print fetched result
            except:
               print ('No data to return')
            
            #loop over all the rows in the table from ISPY
            for x in range(0,len(f)):
               #check if the asteroid already in the database
               if JPL_SPKID[x] in result:
                   #print ('Already in the database')
                   
                   #check how old are the data of the asteroid in the database (if old update them)
                   if JPL_SPKID[x] in result1:
                       
                               sql1 = "UPDATE {0} SET RA='{1[3]}',DEC1='{1[4]}',Special_id='{2}' where JPL_SPKID={1[0]}".format(tab_col[16],f[x],tab_col[18])
                                   
                               try:
                                    # Execute the SQL command
                                    cursor.execute(sql1)
                                    # Commit your changes in the database
                                    db.commit()
                               except:
                                    # Rollback in case there is any error
                                    db.rollback()
                               #loop over all the columns, take care for the empty data columns/rows   
                               for y in range(0,len(tab_col)-4):
                                   if y==0 or y==2 or y==3 or y==4:
                                       sql1=0
                                   elif ma.getmask(f[x][y])==True:
                                        # Prepare SQL query to INSERT a record into the database.
                                        sql1=0
                                        #if data is missing, nothing is imported into the database (the value becomes None)
                                   else:
                                       #fill in(update) the data 
                                        sql1 = "UPDATE [0] SET {1}={2}\
                                        where {3}={4}".format(tab_col[16],tab_col[y],f[x][y],tab_col[0],f[x][0])
                                        
                                        try:
                                            # Execute the SQL command
                                            cursor.execute(sql1)
                                            # Commit your changes in the database
                                            db.commit()
                                        except:
                                            # Rollback in case there is any error
                                            db.rollback()
                                        
                               
               #if the data is not in the database, input them
               else:
                               
                   sql1 = "INSERT INTO {0}(Special_id,JPL_SPKID,Name_designation,\
                                      RA ,\
                                      DEC1 ,Last_Updated)\
                           VALUES ('{2}',{1[0]},'{1[2]}','{1[3]}','{1[4]}',NOW())".format(tab_col[16],f[x],tab_col[18])
                   
                   try:
                       # Execute the SQL command
                       cursor.execute(sql1)
                       # Commit your changes in the database
                       db.commit()
                   except:
                       # Rollback in case there is any error
                       db.rollback()
                   #loop over all the columns  
                   for y in range(0,len(tab_col)-4):
                       if y==0 or y==2 or y==3 or y==4:
                            sql1=0
                       elif ma.getmask(f[x][y])==True:
                            # Prepare SQL query to INSERT a record into the database.
                            sql1=0
                       else:
                            sql1 = "UPDATE {0} SET {1}={2}\
                            where {3}={4}".format(tab_col[16],tab_col[y],f[x][y],tab_col[0],f[x][0])
                            #rint (x,y,f[x][y])
                            try:
                                # Execute the SQL command
                                cursor.execute(sql1)
                                # Commit your changes in the database
                                db.commit()
                            except:
                                # Rollback in case there is any error
                                db.rollback()    
            
            #check if the number of rows in f and in MySQL is the same (so if all the data has been imported)            
            sql2 = "SELECT COUNT(*) FROM {0}".format(tab_col[16])
            
            try:
               # Execute the SQL command
               cursor.execute(sql2)
               # Fetch all the rows in a list of lists.
               result2 = cursor.fetchone()
               # Now check fetched result
               if result2[0]==len(f):
                   print ('For Special ID ',Special_id,': All the data have been recorded into the database.')
               else: 
                   #print ('For Special ID ',Special_id,': The number of rows in the database is not the same as from ISPY')
                   #check why the sizes of tables do not match
                   sql5 ="SELECT {0} from {1}".format(tab_col[0],tab_col[16])
                   try:
                       # Execute the SQL command
                       cursor.execute(sql5)
                       #Fetch all the rows in a list of lists. 
                       result5 = cursor.fetchall()
                       for x in range(0,len(result5)):
                           #check if the asteroid already in the database
                           if result5[x] not in JPL_SPKID:
                                # Prepare SQL query to DELETE required records
                                sql6 = "DELETE FROM {0} WHERE {1}={2}".format(tab_col[16],tab_col[0],result5[x][0])
                                #print (sql6)
                                try:
                                    # Execute the SQL command
                                    cursor.execute(sql6)
                                    # Commit your changes in the database
                                    db.commit()
                                except:
                                    # Rollback in case there is any error
                                    db.rollback()
                                    print('Not possible to delete the outdated data')
                   except:  
                       print ("Error: unable to fetch data to find the reason for not matching tables.")
            except:
               print ('For Special ID ',Special_id,": Error: unable to fetch data")
            try:
               # Execute the SQL command
               cursor.execute(sql2)
               # Fetch all the rows in a list of lists.
               result2 = cursor.fetchone()
               # Now check fetched result
               if result2[0]==len(f):
                   print ('For Special ID ',Special_id,': All the data have been recorded into the database.')
            except:
               print ('For Special ID ',Special_id,": Error: unable to fetch data")  
            # disconnect from server
            db.close()
    return Special_id1