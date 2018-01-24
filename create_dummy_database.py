#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  7 15:18:20 2017

@author: lenka
"""

import pymysql


# Open database connection
db = pymysql.connect("localhost","root","34GH2B." )

# prepare a cursor object using cursor() method
cursor = db.cursor()
#create a database ISPY, if there isnt one like that already
cursor.execute("CREATE DATABASE IF NOT EXISTS ISPY") 
#use the database
cursor.execute("USE ISPY")


# Create table as per requirement
sql = "CREATE TABLE IF NOT EXISTS INPUT_Table (\
  `OBS_id` varchar(20) NOT NULL PRIMARY KEY,\
  `Observation_date` varchar(20) NOT NULL,\
  `Instrument` varchar(20),\
  `Mode` varchar(20),\
  `Vertex1_1` varchar(20),\
  `Vertex1_2` varchar(20),\
  `Vertex2_1` varchar(20),\
  `Vertex2_2` varchar(20),\
  `Vertex3_1` varchar(20),\
  `Vertex3_2` varchar(20),\
  `Vertex4_1` varchar(20),\
  `Vertex4_2` varchar(20),\
  `Status` varchar(20),\
  `Number_of_Asteroids_Detected` INT,\
  `Time_Updated` TIMESTAMP)"

cursor.execute(sql)
# Commit your changes in the database
db.commit()

#input dummy data
sql1= "INSERT INTO INPUT_Table (`OBS_id`,`Observation_date`,`Instrument`,`Vertex1_1`,`Vertex1_2`,`Vertex2_1`,`Vertex2_2`,`Vertex3_1`,`Vertex3_2`,`Vertex4_1`,`Vertex4_2`) VALUES ('170309_134500_M','2017/03/09 13:45:00','MIRI','22 deg','24 deg','2 deg',NULL,NULL,NULL,NULL,NULL)\
,('170809_134500_NS','2017/08/09 13:45:00','NIRSpec','22 deg','24 deg','22 deg','24.2 deg','22.1 deg','24.3 deg','22.4 deg','24 deg')\
,('181209_134500_M','2018/12/09 13:45:00','MIRI','22 deg ','24 deg','2 deg',NULL,'0.2 deg',NULL,'8 deg',NULL)"
#\,('200309_134500_NC','2020/03/09 13:45:00','NIRCam','43 arcmin','56 arcsec','0.3 deg',NULL,NULL,NULL,NULL,NULL)"

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
