# -*- coding: utf-8 -*-
"""
Created on 30/1/2014

Agente que guarda un registro de otros agentes

Guarda los registros como tripletas RDF
Usa OWL-S profile como ontologia

@author: bejar
"""

__author__ = 'bejar'


from  multiprocessing import Process
from flask import Flask,request
from rdflib import Graph, RDF, RDFS, OWL, Namespace, Literal
from rdflib.namespace import FOAF


graph = Graph('Sleepycat')

# first time create the store:
graph.open('./myRDFLibStore', create = True)
graph.close()
acl = Namespace("http://www.nuin.org/ontology/fipa/acl#")
sa = acl.SpeechAct
agn = Namespace("http;//www.agentes.org#")
app = Flask(__name__)
mss_cnt = 0


def shutdown_server():
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

@app.route("/Register")
def register():
    global graph
    global mss_cnt
    message= request.args['content']
    gm = Graph()
    gr = Graph()
    gr.bind('acl',acl)
    gm.parse(data=message)
    print gm.serialize(format='turtle')
    perf = gm.triples( (None,  RDF.type, sa)) # Obtenemos la performativa
    if perf is None:
        gr.add((acl['not-understood'], RDF.type, sa))
    else:
        aresp= gm.subject_objects(FOAF.name)
        a,n = aresp.next()
        print a, n
        ms = acl['message{:{fill}4d}'.format(mss_cnt, fill='0')]
        mss_cnt += 1
        gr.add((ms, RDF.type, sa))
        gr.add((ms, acl.performative, acl.confirm))
        gm.add((agn.juan, FOAF.name, Literal('RegisterAgent')))
        gm.add((ms, acl.sender, agn.RegisterAgent))
        graph.open('./myRDFLibStore')
        graph += gm
    return gr.serialize(format='xml')

@app.route("/Stop")
def stop():
    shutdown_server()


if __name__ == '__main__':
    app.run()
    graph.close()