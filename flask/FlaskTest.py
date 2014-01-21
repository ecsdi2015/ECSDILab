# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 10:47:57 2013

@author: javier
"""

from  multiprocessing import Process
from flask import Flask,request
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"
    
    
@app.route("/agent1", methods=['GET', 'POST'])
def agent1():
    if request.method == 'GET':
        return "This is Agent1"
    else:
        return "Message Received\n"

def webservices():
    app.run()
    
def mainloop():
    print 'MainLoop'
    

if __name__ == "__main__":
    p1=Process(target=webservices)
    p2=Process(target=mainloop)
    p1.start()
    p2.start()