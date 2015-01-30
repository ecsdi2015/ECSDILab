# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 10:47:57 2013

Webservice flask con tres entradas

 / - Responde con Hola mundo
 /pag - pagina web que enseña una pagina con numeros de 0 al 9
 /agent1 - Responde con un mensaje diferente si se recibe un GET o un POST

@author: javier
"""

from  multiprocessing import Process
from flask import Flask, request, render_template
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

@app.route("/pag")
def pag():
    return render_template('file.html', values=range(10))
    
    
@app.route("/agent1", methods=['GET', 'POST'])
def agent1():
    if request.method == 'GET':
        return "This is Agent1"
    else:
        return "Message Received\n"

def mainloop():
    print 'MainLoop'
    

if __name__ == "__main__":
    p1=Process(target=mainloop)
    p1.start()
    app.run()

