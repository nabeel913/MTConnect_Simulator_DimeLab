# -*- coding: utf-8 -*-
"""
Created on Mon Feb 25 03:44:06 2019

@author: smehdi
"""
import asyncio
import pymongo
import psutil
import xml.etree.ElementTree as ET 
import folium


from pymongo import MongoClient

con = MongoClient('152.46.17.251', 27017)
db = con.testdb

my_coll = db.coll_name

#OR do it in the dictonary-style.
emp_name="nabeel"
emp_addr="1312"
emp_id=200226
my_coll = db['coll_name']
my_coll = db.coll_name
emp_rec = {'name':emp_name, 'address':emp_addr, 'id':emp_id}
rec_id = my_coll.insert_one(emp_rec)