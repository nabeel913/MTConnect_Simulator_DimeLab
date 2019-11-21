# -*- coding: utf-8 -*-
"""
Created on Thu Jan 17 09:19:19 2019

@author: smehdi@ncsu.edu
"""

import pandas as pd
master = pd.read_csv('dbs\master.csv')

ports =list(master['agentPorts'])
machines =list(master['machines'])

for port in ports:
    PO=str(port)
    i=(ports.index(port))
    path='temp_folder/Org '+str(i+1)+'/'
    agent = open(path+'agent.py','w+')
    manager = open(path+'manager.py','w')
    weed="{'Content-Type': 'application/xml'}"
    agent.write(f'''from flask import Flask,Response
import xml.etree.ElementTree as ET 
import datetime
from flask import render_template,request
import pandas as pd

def header_update(file):
    utcnow = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    tree = ET.parse(file) 
    root = tree.getroot()
    for elems in root.iter('Header'):
        elems.set('creationTime',str(utcnow))
        j= elems.get('instanceId')
        elems.set('instanceId',str(int(j)+1))
    tree.write(file)
    tree = ET.parse(file) 
    root2 = tree.getroot()
    return root2


def stream(file):
    tree = ET.parse(file) 
    root2 = tree.getroot()
    return root2


def sample(F=0,C=100):
    if F==0:
        buffer=pd.read_csv("buffer.txt",sep='|',names = ["Seq","time", "Mach", "na", "OEE","na2","power","order","qty","partid"])
    if F!=0:
        buffer=pd.read_csv("buffer.txt",sep='|',names = ["Seq","time", "Mach", "na", "OEE","na2","power","order","qty","partid"])
        buffer = buffer = buffer[(buffer.Seq>=int(F))&(buffer.Seq<=int(F)+int(C))]
    buffer=buffer.sort_values(by=['Mach'])
    root = ET.Element("MTConnectStreams")
    doc = ET.SubElement(root, "Streams")
    machs=(buffer.Mach.unique())
    for i in machs:
        xmlpd=(buffer[buffer.Mach==i])
        OEE=list(xmlpd['OEE'])
        seq=list(xmlpd['Seq'])
        time=list(xmlpd['time'])
        for O in range(len(OEE)):
            DS=ET.SubElement(doc, "DeviceStream",timestamp=time[O],sequence=str(seq[O]), name=i).text=str(OEE[O])
            
  
    tree = ET.ElementTree(root)
    tree.write("sample.xml")
    tree = ET.parse("sample.xml") 
    root3 = tree.getroot()
    return root3

app = Flask(__name__)

class MyResponse(Response):
    default_mimetype = 'application/xml'

@app.route('/<path:path>')
def get_sample(path):
    if path=="probe":
        return (ET.tostring(header_update('devices.xml'), encoding='UTF-8').decode('UTF-8'),{weed})
    if path=="current":
        return (ET.tostring(stream('streams.xml'), encoding='UTF-8').decode('UTF-8'),{weed})
    if path=="sample":
        if request.args.get('from')!=None:
            F=int(request.args.get('from'))
            if request.args.get('count')==None:
                C=100
            if request.args.get('count')!=None:
                C=int(request.args.get('count'))
 
            return (ET.tostring(sample(F,C), encoding='UTF-8').decode('UTF-8'),{weed})
        return (ET.tostring(sample(), encoding='UTF-8').decode('UTF-8'),{weed})

if __name__ == "__main__":
        app.run(host='0.0.0.0',port={PO} , threaded=True)''')
    
    agent.close()
    
    
    adpPorts=[a+port for a in (list(range(1,machines[i]+1)))]
    manager.write(f'''
import xml.etree.ElementTree as ET 

import asyncio
import datetime
import time
ports={adpPorts}
file='streams.xml'


try:
    f=open("buffer.txt","r")
    b=f.readlines() 
    if len(b)>0:
        e=b[-1].split('|')
        seq=int(e[0])
except:
    seq=1

@asyncio.coroutine
async def handle_hello(reader, writer):
    global seq
    utcnow= datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    f=open('buffer.txt','a+')
    data = await reader.read(1024)
    SHDR = data.decode('utf-8')
    f.write(str(seq)+"|"+str(utcnow)+"|"+SHDR+"\\n")
    seq=seq+1

    data=(SHDR).split('|')
    m=str(data[0])
    o=str(data[5])
    p=str(data[7])
    q=str(data[6])
    for node in tree.findall("./Streams/DeviceStream[@name='%s']"%m):
        node.set('Order',o)
        node.set('PartID',p)
        node.set('QTY',q)
        utcnow= datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
        
        for a in node.findall('./Events/Power'):
            a.set('timestamp',utcnow)
            a.text=str(data[4])
        tree.write(file)  
        for b in node.findall('./Samples/OEE'):
            b.set('timestamp',utcnow)
            b.text=str(data[2])
    writer.write("Pong".encode("utf-8"))
    writer.close()
    f.seek(0)
    a=f.readlines()
    if(len(a)>1000):
        with open('buffer.txt', 'r') as fin:
            data = fin.read().splitlines(True)
        with open('buffer.txt', 'w') as fout:
            fout.writelines(data[500:])
  
if __name__ == "__main__":

    loop = asyncio.get_event_loop()
    servers = []
    for i in ports:
        #print("Starting server ",i)
        tree = ET.parse(file)
        server = loop.run_until_complete(
                asyncio.start_server(handle_hello, '127.0.0.1', i, loop=loop))   
        tree.write(file)
        
        servers.append(server)
    
    try:
        #print("Running... Press ^C to shutdown")
        #run loops of servers
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    for i, server in enumerate(servers):
        #print("Closing server ",i)
        #if key pressed close all servers.
        server.close()
        loop.run_until_complete(server.wait_closed())
    loop.close()       
        ''')
    manager.close()
    start=open(path+'/startAgent.bat','w')
    stop=open(path+'/stopAgent.bat','w')
    

    start.write(f'start /min "[O{i}agent]" python agent.py\nstart /min "[O{i}manager]" python manager.py')
    start.close()
    stop.write(f'taskkill /f /FI "WINDOWTITLE eq [O{i}agent]\ntaskkill /f /FI "WINDOWTITLE eq [O{i}manager]')
    stop.close()
    