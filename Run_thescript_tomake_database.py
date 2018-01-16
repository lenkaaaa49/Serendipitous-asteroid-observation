#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 16:23:52 2017

@author: lenka
"""

import pymysql
import import_data

#get all the names of the new made tables and run all the functions to 
#create the database and tables
Special_id,Table_names=import_data.importDATA()
print ('Table names:',Table_names)