
import os
import pandas as pd
import shutil
import time
import subprocess


master = pd.read_csv('dbs\master.csv')
orgs = list(master['names'])
DIR=(os.getcwd())

def father():
    subprocess.call(['python', 'father.py'])
 
def master():
    subprocess.call(['python', 'master_init.py'])

def moadp():
    subprocess.call(['python', 'mother_adp.py'])

def moagent():
    os.chdir(DIR)
    os.system("python mother_agents.py")
def momap():
    os.chdir(DIR)
    os.system("python mother_map.py")
def moxml():
    os.chdir(DIR)
    os.system("python mother_xmls.py")
def index():
    p=subprocess.Popen(['python', 'index.py'])
    print(p.pid)
    
    
def init():
    os.chdir(DIR)
    os.startfile("init.bat")
    os.chdir(DIR)
    
def startAgent():
    master = pd.read_csv('dbs\master.csv')
    orgs = list(master['names'])
    for i in range(len(orgs)):
        path=DIR+'/temp_folder/Org '+str(i+1)+'/'
        os.chdir(path)
        os.startfile("startAgent.bat")
        os.chdir(DIR)
    
def startAdps():
    master = pd.read_csv('dbs\master.csv')
    orgs = list(master['names'])
    for i in range(len(orgs)):
        path=DIR+'/temp_folder/Org '+str(i+1)+'/'
        os.chdir(path)
        os.startfile("batchStart.bat")
        os.chdir(DIR)

def stopAgent():
    import pymongo
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["mtconnectdatabase"]
    mycol = mydb["orders"]
    mycol.drop()
    master = pd.read_csv('dbs\master.csv')
    orgs = list(master['names'])
    for i in range(len(orgs)):
        path=DIR+'/temp_folder/Org '+str(i+1)+'/'
        os.chdir(path)
        os.startfile("stopAgent.bat")
        os.chdir(DIR)
        
def stopAdps():
     for i in range(len(orgs)):
        path=DIR+'/temp_folder/Org '+str(i+1)+'/'
        os.chdir(path)
        os.startfile("batchKill.bat")
        os.chdir(DIR)

def reset():
   
  dirpath=DIR+'/temp_folder/'
          
  for filename in os.listdir(dirpath):
    filepath = os.path.join(dirpath, filename)
    try:
        shutil.rmtree(filepath)
    except OSError:
        os.remove(filepath)
        
def STOP():
    stopAgent()
    stopAdps()
    
def START():
    startAgent() 
    time.sleep(7)
    startAdps()

#STOP()
#startAdps()
#reset()
#init()
#father()
#master()
#moadp()
#moagent()
#momap()
#moxml()
#startAgent()
#stopAdps()
#index()
#stopAgent()

