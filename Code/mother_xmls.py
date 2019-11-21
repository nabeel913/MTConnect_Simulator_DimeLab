# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 11:57:34 2019

@author: smehdi@ncsu.edu
"""

import pandas as pd
master = pd.read_csv('dbs\master.csv')
from father import cncBrands as cncBrands
import xml.etree.ElementTree as ET 
import random
import datetime
time=datetime.datetime.utcnow()

ports =list(master['agentPorts'])
machines =list(master['machines'])

for port in ports:
    PO=str(port)
    O=(ports.index(port))
    M=machines[O]
    dir='temp_folder/Org '+str(O+1)+'/'
    path='temp_folder/Org '+str(O+1)+'/devices.xml'
    D=open(path,'w')
    D.write("""<MTConnectDevices>
	<Header creationTime="{}" instanceId="0" sender="localhost" version="1.1" />
	<Devices>
    </Devices>
</MTConnectDevices>""".format(time))
    D.close()
    
    streamPath='temp_folder/Org '+str(O+1)+'/streams.xml'
    S=open(streamPath,'w')
    S.write(("""<MTConnectStreams>
	<Header creationTime="{}" instanceId="0" sender="localhost" version="1.1" />
	<Streams>
	</Streams>
</MTConnectStreams>""".format(time)))
    S.close()
    
    
    adpPorts=[a+port for a in (list(range(1,M+1)))]
    
    tree = ET.parse(path)
    root = tree.getroot()
    
    
    OEMList = []
    f = open(dir+'config.cfg','w')
    portsList = adpPorts
    for i in range(M):
        for item in root.iter('Devices'):
            
            OEM = random.choice(cncBrands)
            OEMList.append(OEM)
            name = "Mach"+str(i+1)
            id1 = str(i+1)+'.1'
            id2 = str(i+1)+'.2'
            ID = 'O'+str(O+1)+'M'+str(i+1)
            adapter = name + ' Port:'+ str(portsList[i]) + str('\n')
            f.write(adapter)
            de = ET.Element("Device")
            de.tag = "Device"
            de.text=" "
            de.set('id',ID)
            de.set('name',name)
            de.set('OEM',OEM)
            da = ET.SubElement(de, "Dataitems")
            dc = ET.SubElement(da, "Dataitem")
            dc.set('category','EVENT')
            dc.set('ID',id1)
            dc.set('name','power')
            db = ET.SubElement(da, "Dataitem")
            db.set('category','SAMPLE')
            db.set('ID',id2)
            db.set('name','OEE')
        
            item.append(de)
            
    tree.write(path)
    f.close()
    
    tree = ET.parse(streamPath)
    root = tree.getroot()
    for i in range(M):
        for item in root.iter('Streams'):
            
            name = "Mach"+str(i+1)
            id1 = str(i+1)+'.1'
            id2 = str(i+1)+'.2'
            ID = 'O'+str(O+1)+'M'+str(i+1)
            
            de = ET.Element("DeviceStream")
            de.tag = "DeviceStream"
            de.text=" "
            de.set('id',ID)
            de.set('name',name)
            de.set('Order',"UNAVAILABLE")
            de.set('QTY',"UNAVAILABLE")
            de.set('PartID',"UNAVAILABLE")
            de.set('id',ID)
            de.set('name',name)
            de.set('OEM',OEMList[i])
            da = ET.SubElement(de, "Events")
            dp = ET.SubElement(da, "Power")
            dp.set('dataItemID',id1)
            dp.set('timestamp','TSP')
            dp.set('name','power')
            dp.text="UNAVAILABLE"
            
            db = ET.SubElement(de, "Samples")
            dq = ET.SubElement(db, "OEE")
            dq.set('dataItemID',id2)
            dq.set('timestamp','TSP')
            dq.set('name','OEE')
            dq.text="UNAVAILABLE"
           
        
            item.append(de)
    
    tree.write(streamPath)
    
    
   

     





