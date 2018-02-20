#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 16:23:52 2017

@author: lenka
"""

import Choosing_Function
import Different_Functions
from DateTime import Timezones, DateTime
zones = set(Timezones())

lambdaMu=[3.6,15,20]#wavelenghts until 29.9999 and only 4 decimal points
#eta=1.3
#pv=0.2
#relative_reflectance=1.4

#get all the names of the new made tables and run all the functions to 
#create the database and tables
#Special_id=Choosing_Function.choose_function('34GH2B.',3,DateTime('2018/01/23 16:56:00 '))
#need:  password to MYSQL database
#       function number (1-4)
#       date and time in DateTime to determine which tables are outdated (if data older than this, they are updated)
#               can be empty for function 1 and 3
#print ('Table names:',Special_id)

#run the functions
#Special_id=Different_Functions.create_new_tables('Login_Data.txt','Input_Data.txt',lambdaMu)
#add new lines (new data) in the database

#Special_id=Different_Functions.update_old_tables('Login_Data.txt','Input_Data.txt',DateTime('2018/02/02 11:36:00 ZULU'),lambdaMu)
#go over data older than xyDate and update them/add them

Special_id=Different_Functions.add_and_update_tables('Login_Data.txt','Input_Data.txt',lambdaMu)
#adds new data and updates all the outdated ones 

#Special_id=Different_Functions.add_and_update_tables_after_date('Login_Data.txt','Input_Data.txt',DateTime('2018/01/23 16:56:00'),lambdaMu)
#adds new data and go over data older than xyDate and update them/add them