#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 10:38:55 2018

@author: lenka
"""
def Get_user_password(Login_file):

    f = open(Login_file, 'r')
        
    #look for the user name and password
    for idx,line in enumerate(f.readlines()): #number the lines
            if line.find('User name') > -1: #find the user name
                user=line.split(':')
                user= user[1].strip('\n')
                user= user.strip(' ')
                #print (user)
                
            elif line.find('Password') > -1: #find the password
                password=line.split(':')
                password= password[1].strip(' ')
                
            else:
                print ('Password or user name is missing')
                    
    return user,password

def Get_inputs(Input_file):

    f = open(Input_file, 'r')
        
    #look for the user name and password
    for idx,line in enumerate(f.readlines()): #number the lines
            if line.find('Beaming parameter') > -1: #find the user name
                eta=line.split(':')
                #print (eta[1])
                
            elif line.find('Albedo') > -1: #find the password
                pv=line.split(':')
                #print (pv[1])
                
            elif line.find('Relative reflectance') > -1: #find the password
                ref_parameter=line.split(':')
                #print (ref_parameter[1])
                
            else:
                print ('Data missing')
            
    return eta[1],pv[1],ref_parameter[1]


           
       