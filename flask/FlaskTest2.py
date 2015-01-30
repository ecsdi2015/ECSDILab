# -*- coding: utf-8 -*-
"""
Created on Thu Dec 26 10:47:57 2013

Webservice flask con una entrada

/agente - Retorna la suma de los dos numeros que se pasan como parametros x e y de la peticion

@author: javier
"""
__author__ = 'bejar'

from flask import Flask,request
app = Flask(__name__)

@app.route("/agente")
def agent1():
    x = int(request.args['x'])
    y = int(request.args['y'])
    return str(x+y)

if __name__ == '__main__':
    app.run()