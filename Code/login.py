from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort
import os
import subprocess

import time
#https://pythonspot.com/login-authentication-with-flask/
app = Flask(__name__)

RUN=0

def string2int(string):
    sum=0
    for i in string:
        sum+=ord(i)
    return(sum)
    

def controlPanel(ORGS,MACHS,SEED):
    f=open("control_panel.py","w")
    f.write(f"""ORGS={ORGS}
MACHS={MACHS}
seed={SEED}""")
    f.close()
    
@app.route('/home',methods = ['POST', 'GET'])
def result():
    global RUN
    RUN=1
    if request.method == 'POST':
     
      ORGS=int(request.form["org"])
      Low=int(request.form["low"])
      High=int(request.form["high"])
      MACHS=[Low,High]
      SEED=string2int(request.form["seed"])
      controlPanel(ORGS,MACHS,SEED)
      p = subprocess.Popen(["python","autostart.py"])
      returncode = p.wait()
      estime= ORGS*High/10
      result = {'Orgs': ORGS, 'Range of Machines':str(MACHS),'Random Seed':str(SEED),'Estimated Seconds to start':estime}
      return render_template("home.html",result = result)
    
@app.route('/')
def home():
    if not session.get('logged_in'):
        return (render_template('login.html'))
    else:
        return render_template('input.html')
        #return ('Hello Boss!  <a href="/logout">Logout</a>')
        
@app.route('/view')
def show_map():
    if (session.get('logged_in')!=False)and (RUN==1):
        return render_template('view.html')
    if (session.get('logged_in')!=False)and (RUN==0):
        return ("system not initiated yet")
    else:
        return("please login first")

@app.route('/stop')
def stop():
    global RUN
    RUN=0
    import autoswitches
    autoswitches.stopAgent()
    return ("Simulation Stopped")

@app.route('/reset')
def reset():
    import autoswitches
    autoswitches.reset()
    return ("System Reset")
 
@app.route('/login', methods=['POST'])
def do_admin_login():
    
    if (request.form['password'] == 'dime123' and request.form['username'] == 'user'):
        session['logged_in'] = True
        
    else:
        flash('wrong password!')
    return home()
 
@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()



if __name__ == "__main__":
    app.secret_key = os.urandom(4)
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True,host='0.0.0.0', port=5000)