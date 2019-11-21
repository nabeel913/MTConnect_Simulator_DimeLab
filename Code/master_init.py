# -*- coding: utf-8 -*-
"""
Created on Thu Dec  6 14:19:20 2018

@author: smehdi@ncsu.edu
"""
import pandas as pd
import random as random

import numpy as np
from control_panel import ORGS as ORGS
from control_panel import MACHS as MACHS
from control_panel import seed as seed



US_COORDINATES = (39.0902,-98.7129)




data = pd.read_csv('dbs\gps.csv')
#data=dta.loc[dta['state'] == 'Texas']

random.seed(seed)

randCity = random.sample(range(len(data)),ORGS)
#weather = Weather(unit=Unit.CELSIUS)
names=['Org '+str(i) for i in list(range(1,ORGS+1))]
master=(data.iloc[randCity][['latitude','longitude','city','state','population']])
machines=np.random.randint(MACHS[0],MACHS[1],len(master))
machines=((machines).astype(int))
master['names']=names
master['machines']=machines



def weatherUpdate():
    temp=[]
    atmo=[]
    for i in range(len(master)):
        #location = weather.lookup_by_latlng(master.iloc[i]['latitude'],master.iloc[i]['longitude'])
        #condition = location.condition
        #temp.append(int(condition.temp))
        #atmo.append(str(condition.text))
        temp.append(random.randint(-15,40))
        states=['Rain','Sunny','Cloudy','Red','Green','Snow','Hot','Shiny','Dark','Bright']
        atmo.append(random.choice(states))
    master['temperature']=temp
    master['atmosphere']=atmo


def capacityUtilization():
    CU=[]
    for i in range(len(master)):
        M=master.iloc[i]['atmosphere']
        C=M.split()

        if('Rain'in C) or  ('Showers'in C) or ('Snow' in C):
            CU.append(0)
        else:
            c=(int(50+100*master.iloc[i]['temperature']/master['temperature'].max()))
            if c>=100:
                c=100
            CU.append(abs(c))
    master['CapacityUtil']=CU
    
def flaskAgents():
    ports = list(range(9000,20000,100)) #Expose ports through firewall
    portsList = random.sample(ports, ORGS)
    master['agentPorts']=portsList
        
    

def updateCSV():
    weatherUpdate()#1
    capacityUtilization()#2
    flaskAgents()#3
    master.to_csv('dbs\master.csv')
    
#could update every 10 minutes or so  
updateCSV()
