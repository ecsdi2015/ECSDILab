# -*- coding: utf-8 -*-
"""
filename: SimplePersonalAgent

Ejemplo de agente que busca en el directorio y llamma al agente obtenido


Created on 09/02/2014

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
port = 9002

# Flask stuff
app = Flask(__name__)

# Configuration constants and variables
agn = Namespace("http://www.agentes.org#")

# Contador de mensajes
mss_cnt = 0

# Datos del Agente
agentname = 'AgentePersonal'
agn_uri = agn.AgenteInfo
agn_addr = 'http://' + hostname + ':'+str(port)+'/comm'
self_stop = 'http://' + hostname + ':'+str(port)+'/Stop'

# Directory agent address
ra_address = "http://" + hostname + ":9000/Register"
ra_stop = 'http://' + hostname + ':9000/Stop'
ra_uri = agn.Directory

# Global dsgraph triplestore
dsgraph = Graph()



def directory_search_message(type):
    """
    Busca en el servicio de registro mandando un
    mensaje de request con una accion Seach del servicio de directorio

    Podria ser mas adecuado mandar un query-ref y una descripcion de registo
    con variables

    :param gmess:
    :return:
    """
    global mss_cnt

    gmess = Graph()

    gmess.bind('foaf', FOAF)
    gmess.bind('dso', DSO)
    reg_obj = agn[agentname+'-search']
    gmess.add((reg_obj, RDF.type, DSO.Search))
    gmess.add((reg_obj, DSO.AgentType,type))

    gr = send_message(
            build_message(gmess, perf= ACL.request,
                      sender= agn_uri,
                      receiver= ra_uri,
                      content= reg_obj,
                      msgcnt= mss_cnt),
            ra_address)
    mss_cnt += 1
    return gr


def infoagent_search_message(addr,ragn_uri):
    """
    Envia una accion a un agente de informacion
    """
    global mss_cnt

    gmess = Graph()

    # Supuesta ontologia de acciones de agentes de informacion
    IAA = Namespace('IAActions')

    gmess.bind('foaf', FOAF)
    gmess.bind('iaa', IAA)
    reg_obj = agn[agentname+'-info-search']
    gmess.add((reg_obj, RDF.type, IAA.Search))

    gr = send_message(
            build_message(gmess, perf= ACL.request,
                      sender= agn_uri,
                      receiver= ragn_uri,
                      msgcnt= mss_cnt),
            addr)
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

    # Buscamos en el directorio
    # un agente de hoteles
    gr = directory_search_message( DSO.HotelsAgent)
    print gr.serialize(format='turtle')

    # Obtenemos la direccion del agente de la respuesta
    # No hacemos ninguna comprobacion sobre si es un mensaje valido
    msg = gr.value(predicate= RDF.type, object= ACL.FipaAclMessage)
    content = gr.value(predicate= msg, predicate= ACL.content)
    ragn_addr = gr.value(object= content, predicate= DSO.Address)
    rgan_uri = gr.value(object= content, predicate= DSO.Uri)

    # Ahora mandamos un objeto de tipo request mandando una accion de tipo Search
    # que esta en una supuesta ontologia de acciones de agentes
    infoagent_search_message(ragn_addr,ragn_uri)


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

