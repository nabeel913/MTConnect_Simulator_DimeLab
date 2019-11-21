# -*- coding: utf-8 -*-
import pandas as pd
import random
from math import floor
master = pd.read_csv('dbs\master.csv')

#////////////////////////////////////////////////""
import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mtconnectdatabase"]
mycol = mydb["orders"]
orders = []
orderType=['A','B','C','D','E','E2','F','F4','GZ','G']
#////////////////////////////////////////////////""

orgs = list(master['names'])
machs = list(master['machines'])
cu = list(master['CapacityUtil'])
ports =list(master['agentPorts'])
batchNumbers=random.sample(range(20000,100000),(sum(machs)))
indexBatch=0
for i in range(len(orgs)):
    path='temp_folder/'+str(orgs[i])+'/adapters/'
    machines=machs[i]
    capacity=cu[i]
    Aport=ports[i]
    ON=floor((capacity*machines)/100)
    count=1
    pathOrg='temp_folder/'+str(orgs[i])+'/'
    batch = open(pathOrg+'batchStart.bat','w+')
    kill = open(pathOrg+'batchKill.bat','w+')
    
    
    for m in range(machines):
        #//////
       
        t=random.sample(orderType,1)
        name='Mach'+str(m+1)
        MID=str(i+1)+name
        order= { "_id": MID, "QTY": random.randint(100,4000), "PartID": t[0],"Order":batchNumbers[indexBatch]}
        orders.append(order)
        
        #/////
        mId=str(m+1)
        fpath=path+'Mach'+mId+'.py'
        
        f = open(fpath,'w')
        port= Aport+m+1
        if count<=ON:
            mState = 'ON'
            count+=1
        else:
            mState='OFF'
            count+=1
        indexBatch+=1   
   
        weed='{ "_id": M }'
        f.write(f'''import socket
import time
import random
HOST = '127.0.0.1'
PORT = {port}

import pymongo
myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["mtconnectdatabase"]
mycol = mydb["orders"]
M="{MID}"
myquery = {weed}


while True:
    mydoc = mycol.find(myquery)
    for x in mydoc:
      order= ((x['Order']))
      QTY=((x['QTY']))
      PartID=((x['PartID']))
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        data=random.randint(50,95)
        breakdown=random.paretovariate(1)
        bd=0
        c=0
        if isinstance(order,str):
            ran = "{name}|OEE|"+"UNAVAILABLE"+"|power|UNAVAILABLE"+"|Idle|Empty|UNAVAILABLE"
        if isinstance(order,int):    
            if('{mState}'=='OFF'):
                data=0
            if('{mState}'!='OFF') and (breakdown>=2) and (breakdown<=500):
                ran = "{name}|OEE|"+str(data)+"|power|Cutting|"+str(order)+"|"+str(QTY)+"|"+PartID
                c=1
            if(c==0):
                ran = "{name}|OEE|"+str(data)+"|power|{mState}|"+str(order)+"|"+str(QTY)+"|"+PartID
       
        if breakdown>500:  
            ran = "{name}|OEE|"+"UNAVAILABLE"+"|power|BREAKDOWN|"+str(order)+"|"+str(QTY)+"|"+PartID
            bd=1
                  
        time.sleep(1)
        strin=bytes(ran,encoding='utf-8')
        s.sendall(strin)
        if(bd==1):
           repairTime=random.randint(50,100)
           while repairTime>=1:
               time.sleep(1)
               repairTime-=1
           bd=0

''')
        id="O"+str(i)+"M"+str(m)
        batch.write(f'start /min "[{id}]" python adapters/Mach{mId}.py\n')
        kill.write(f'taskkill /f /FI "WINDOWTITLE eq [{id}]\n')
            

batch.close()
kill.close()
f.close()
x = mycol.insert_many(orders)

