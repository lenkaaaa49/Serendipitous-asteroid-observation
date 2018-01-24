#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 16:23:52 2017

@author: lenka
"""

import Choosing_Function
from DateTime import Timezones, DateTime
zones = set(Timezones())

#get all the names of the new made tables and run all the functions to 
#create the database and tables
Special_id=Choosing_Function.choose_function('34GH2B.',3,DateTime('2018/01/23 16:56:00'))
#need:  password to MYSQL database
#       function number (1-4)
#       date and time in DateTime to determine which tables are outdated (if data older than this, they are updated)
#               can be empty for function 1 and 3
#print ('Table names:',Special_id)
