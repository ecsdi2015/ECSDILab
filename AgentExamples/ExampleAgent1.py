# -*- coding: utf-8 -*-
"""
filename: ExampleAgent1

Agente que se registra, busca en el registro un agente y le envia un mensaje

Created on 08/02/2014

@author: javier
"""

__author__ = 'javier'


from  multiprocessing import Process
import socket

from flask import Flask, render_template, request, url_for
from rdflib import Graph, Namespace, Literal, URIRef, BNode
from rdflib.namespace import FOAF, RDF
import requests

from OntoNamespaces import ACL, DSO
from AgentUtil import shutdown_server
from ACLMessages import build_message, send_message

# Configuration stuff
hostname = socket.gethostname()
port = 9001

# Flask stuff
app = Flask(__name__)

# Configuration constants and variables
agn = Namespace("http://www.agentes.org#")
mss_cnt = 0
agentname = 'Agente1'
agn_uri = agn.Agente1
agn_addr = 'http://' + hostname + ':9001/comm'

self_stop = 'http://' + hostname + ':'+str(port)+'/Stop'


# Register agent address
ra_address = "http://" + hostname + ":9000/Register"
ra_stop = 'http://' + hostname + ':9000/Stop'
ra_uri = agn.Directory

dsgraph = Graph() # Global dsgraph triplestore


def register_message():
    """
    Envia un mensaje de registro al servicio de registro


    :param gmess:
    :return:
    """
    global mss_cnt

    gmess = Graph()

    gmess.bind('foaf', FOAF)
    gmess.bind('dso', DSO)
    reg_obj = agn['Agent1-Register']
    gmess.add((reg_obj, RDF.type, DSO.Register))
    gmess.add((reg_obj, DSO.Uri, agn_uri))
    gmess.add((reg_obj, FOAF.Name, Literal(agentname)))
    gmess.add((reg_obj, DSO.Address, Literal(agn_addr)))
    gmess.add((reg_obj, DSO.AgentType, DSO.HotelsAgent))

    gr = send_message(
            build_message(gmess, perf= ACL.request,
                      sender= agn_uri,
                      receiver= ra_uri,
                      content= reg_obj,
                      msgcnt= mss_cnt),
            ra_address)
    mss_cnt += 1

    return gr

def search_message():
    """
    Busca en el servicio de registro


    :param gmess:
    :return:
    """
    global mss_cnt

    gmess = Graph()

    gmess.bind('foaf', FOAF)
    gmess.bind('dso', DSO)
    reg_obj = agn['Agent1-search']
    gmess.add((reg_obj, RDF.type, DSO.Search))
    gmess.add((reg_obj, DSO.AgentType, DSO.HotelsAgent))

    gr = send_message(
            build_message(gmess, perf= ACL.request,
                      sender= agn_uri,
                      receiver= ra_uri,
                      content= reg_obj,
                      msgcnt= mss_cnt),
            ra_address)
    mss_cnt += 1

    return gr


@app.route("/iface", methods=['GET','POST'])
def browser_iface():
    """
    Permite la comunicacion con el agente via un navegador
    via un formulario
    """
    if request.method == 'GET':
        return render_template('iface.html')
    else:
        user = request.form['username']
        mess = request.form['message']
        return render_template('riface.html', user= user, mess= mess)

@app.route("/Stop")
def stop():
    """
    Entrypoint que para el agente

    :return:
    """
    tidyup()
    shutdown_server()
    return "Parando Servidor"

@app.route("/comm")
def comunicacion():
    """
    Entrypoint de comunicacion del agente
    """
    return "Hola"

def tidyup():
    """
    Acciones previas a parar el agente

    """
    pass
    #dsgraph.close()


def agentbehavior1():
    """
    Un comportamiento del agente

    :return:
    """
    # Registramos el agente
    gr = register_message()
    print gr.serialize(format='turtle')

    gr = search_message()
    print gr.serialize(format='turtle')


    # r = requests.get(ra_stop)
    # print r.text

    # Selfdestruct
    requests.get(self_stop)

if __name__ == '__main__':
    # Ponemos en marcha los behaviors
    ab1=Process(target=agentbehavior1)
    ab1.start()

    # Ponemos en marcha el servidor
    app.run(host=hostname, port=port)

    # Esperamos a que acaben los behaviors
    ab1.join()
    print 'The End'
