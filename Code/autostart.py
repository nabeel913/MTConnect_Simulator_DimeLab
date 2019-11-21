# =============================================================================
# SOURCE CODE
# """"
# p = subprocess.Popen(["python", "index.py"])
# returncode = p.wait()
# print ("Process ID of subprocess %s" % p.pid)
# 
# # Send SIGTER (on Linux)
# p.terminate()
# # Wait for process to terminate
# returncode = p.wait()
# print ("Returncode of subprocess: %s" % returncode)
# 
# subprocess.call(['python', 'father.py'])
# =============================================================================
import subprocess
import time
import psutil
import pandas as pd
import autoswitches
master = pd.read_csv('dbs\master.csv')
orgs = list(master['names'])
machs = list(master['machines'])



def kill(proc_pid):
    process = psutil.Process(proc_pid)
    for proc in process.children(recursive=True):
        proc.kill()
    process.kill()

def setup():
     
    files=["father.py","master_init.py","mother_adp.py","mother_agents.py", "mother_map.py","mother_xmls.py"]
    for file in files:
        p = subprocess.Popen(["python",file])    
        if (file=='index.py'):
            #print(f"{file} done")
            #print("starting view....")
            break
        returncode = p.wait()
    #print(f"{file} done")

setup()
autoswitches.startAgent()
##print("starting agents...")
time.sleep(3+len(orgs)/2)
autoswitches.startAdps()
#print("starting adapters...")
    

#def killall():
#    for i in pidList:
#        kill(i)
#        
#while True:
#    cmd = input("What?")
#    if (cmd=='kill'):
#        p.terminate()
#        returncode = p.wait()
#        autoswitches.stopAgent()
#        print ("stopping view")
#        break
#    else:
#        print("invalid cmd")



