#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 16:23:52 2017

@author: lenka
"""

import pymysql
import import_data_toMSQLtable

#get all the names of the new made tables and run all the functions to 
#create the database and tables
Special_id=import_data_toMSQLtable.importDATA('34GH2B.')
print ('Table names:',Special_id)