# -*- coding: utf-8 -*-
"""
filename: SimpleRegisterAgent

Agente que lleva un registro de otros agentes

Utiliza un registro simple que guarda en un grafo RDF

El registro no es persistente y se mantiene mientras el agente funciona


Created on 08/02/2014

@author: javier
"""

__author__ = 'javier'

from  multiprocessing import Process, Queue
import socket

from flask import Flask, request, render_template
from rdflib import Graph, RDF, Namespace, Literal, RDFS
from rdflib.namespace import FOAF

from OntoNamespaces import ACL, DSO
from AgentUtil import shutdown_server
from ACLMessages import is_message, send_message, get_performative

# Configuration stuff
hostname = socket.gethostname()
port = 9000

# Directory Service Graph
dsgraph = Graph()

# Vinculamos todos los espacios de nombre a utilizar
dsgraph.bind('acl', ACL)
dsgraph.bind('rdf', RDF)
dsgraph.bind('rdfs', RDFS)
dsgraph.bind('foaf', FOAF)
dsgraph.bind('dso', DSO)


agn = Namespace("http://www.agentes.org#")
app = Flask(__name__)
mss_cnt = 0

cola1 = Queue() # Cola de comunicacion entre procesos


@app.route("/Register")
def register():
    """
    Entry point del agente que recibe los mensajes de registro
    La respuesta es enviada por el servidor,
    No hay necesidad de enviar el mensaje a la direccion del agente

    :return:
    """




    global dsgraph
    global mss_cnt
    #Extraemos el mensaje y creamos un grafo con el
    message= request.args['content']
    gm = Graph()
    gm.parse(data=message)

    # Creamos un grafo para la respuesta
    gr = Graph()
    gr.bind('acl',ACL)

    print gm.serialize(format='turtle')

    # Obtenemos la performativa

    # Comprobamos que sea un mensaje FIPA ACL
    if not is_message(gm):
        # Si no es respondemos que no hemos entendido el mensaje
        gr.add((ACL['not-understood'], RDF.type, ACL.Speechact))
    else:
        perf = get_performative(gm)
        if perf != ACL.request:
           # Si no es respondemos que no hemos entendido el mensaje
            gr.add((ACL['not-understood'], RDF.type, ACL.Speechact))

        else:
            # Si la hay extrameos el nombre del agente (FOAF.Name) y el URI agente
            aresp= gm.subject_objects(FOAF.name)
            a,n = aresp.next()
            print a, n


            ms = ACL['message{:{fill}4d}'.format(mss_cnt, fill='0')]
            mss_cnt += 1
            gr.add((ms, RDF.type, ACL.Speechact))
            gr.add((ms, ACL.performative, ACL.confirm))
            gm.add((agn.juan, FOAF.name, Literal('RegisterAgent')))
            gm.add((ms, ACL.sender, agn.RegisterAgent))

        dsgraph += gm
    return gr.serialize(format='xml')


@app.route('/info')
def info():
    """
    Entrada que da informacion sobre el agente
    """
    global dsgraph
    global mss_cnt

    return render_template('info.html',nmess= mss_cnt, graph= dsgraph.serialize(format='turtle'))


@app.route("/Stop")
def stop():
    """
    Entrada que para el agente
    """
    print 'Parando Servidor'
    tidyup()

    shutdown_server()
    return "Parando Servidor"

def tidyup():
    pass
    #dsgraph.close()

def agentbehavior1(cola):
    """
    Behaviour que simplemente espera mensajes de una cola y los imprime
    """
    fin = False
    while not fin:
        while cola.empty():
            pass
        v = cola.get()
        print v

if __name__ == '__main__':
    # Ponemos en marcha los behaviours como procesos
    ab1=Process(target=agentbehavior1,args=(cola1,))
    ab1.start()

    # Ponemos en marcha el servidor Flask
    app.run(host= hostname, port= port)

    # Cerramos los procesos
    ab1.terminate()

    print 'The End'

