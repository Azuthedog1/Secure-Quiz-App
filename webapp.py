import os
import time
from flask import Flask, url_for, render_template, request
from flask import redirect
from flask import session

app = Flask(__name__)

# In order to use "sessions",you need a "secret key".
# This is something random you generate.  
# For more info see: https://flask.palletsprojects.com/en/1.1.x/config/#SECRET_KEY

app.secret_key=os.environ["SECRET_KEY"]; #This is an environment variable.  
                                     #The value should be set in Heroku (Settings->Config Vars).  
                                     #To run locally, set in env.sh and include that file in gitignore so the secret key is not made public.


@app.route('/')
def renderMain():
    global x
    x = 0
    global z
    z = str()
    return render_template('home.html')

@app.route('/startOver')
def startOver():
    session.clear() #clears variable values and creates a new session
    return redirect(url_for('renderMain')) # url_for('renderMain') could be replaced with '/'

@app.route('/page1')
def renderPage1():
    global start
    start = time.time()
    return render_template('page1.html')

@app.route('/page2',methods=['GET','POST'])
def renderPage2():
    session["quest1"]=request.form['question1']
    return render_template('page2.html')

@app.route('/page3',methods=['GET','POST'])
def renderPage3():
    session["quest2"]=request.form['question2']
    return render_template('page3.html')

@app.route('/results',methods=['GET','POST'])
def renderResults():
    session["quest3"]=request.form['question3']
    end = time.time()
    y = (end-start)
    return render_template('results.html', correct = getScore(), incorrect = getScore2(), time = int(y))

def getScore():
    x = 0
    try:
        int(session["quest1"])
        if int(session["quest1"]) == 2021:
            x = x + 1
    except ValueError:
        pass
    try:
        int(session["quest2"])
        if int(session["quest2"]) == 15:
            x = x + 1 
    except ValueError:
        pass
    if str(session['quest3']) == "purple":
        x = x + 1
    return x

def getScore2():
    z = str()
    try:
        int(session["quest1"])
        if int(session["quest1"]) == 2021:
            pass
        else:
            z = "one "
    except ValueError:
        z = z + "one "
    try:
        int(session["quest2"])
        if int(session["quest2"]) == 15:
            pass
        else:
            z = z + "two " 
    except ValueError:
        z = z + "two "
    if str(session['quest3']) == "purple":
        pass
    else:
        z = z + "three "
    print(z)
    return z



if __name__=="__main__":
    app.run(debug=True)
