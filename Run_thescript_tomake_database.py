#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 16:23:52 2017

@author: lenka
"""

import Choosing_theFunction
from DateTime import Timezones, DateTime
zones = set(Timezones())

#get all the names of the new made tables and run all the functions to 
#create the database and tables
Special_id=Choosing_theFunction.choose_function('34GH2B.',3,DateTime('2018/01/17 15:50:00'))
print ('Table names:',Special_id)
