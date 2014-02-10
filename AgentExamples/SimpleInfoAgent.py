# -*- coding: utf-8 -*-
"""
filename: ExampleAgent1

Agente que se registra como agente de hoteles y espera peticiones

Created on 08/02/2014

@author: javier
"""
__author__ = 'javier'

from  multiprocessing import Process, Queue
import socket

from flask import Flask, render_template, request, url_for
from rdflib import Graph, Namespace, Literal, URIRef, BNode
from rdflib.namespace import FOAF, RDF
import requests

from OntoNamespaces import ACL, DSO
from AgentUtil import shutdown_server
from ACLMessages import build_message, send_message, get_message_properties

# Configuration stuff
hostname = socket.gethostname()
port = 9001

# Flask stuff
app = Flask(__name__)

# Configuration constants and variables
agn = Namespace("http://www.agentes.org#")

# Contador de mensajes
mss_cnt = 0

# Datos del Agente
agentname = 'AgenteInfo1'
agn_uri = agn.AgenteInfo
agn_addr = 'http://' + hostname + ':'+str(port)+'/comm'
self_stop = 'http://' + hostname + ':'+str(port)+'/Stop'

# Directory agent address
ra_address = "http://" + hostname + ":9000/Register"
ra_stop = 'http://' + hostname + ':9000/Stop'
ra_uri = agn.Directory

# Global dsgraph triplestore
dsgraph = Graph()

# Cola de comunicacion entre procesos
cola1 = Queue()

def register_message():
    """
    Envia un mensaje de registro al servicio de registro
    usando una performativa Request y una accion Register del
    servicio de directorio

    :param gmess:
    :return:
    """
    global mss_cnt

    gmess = Graph()

    # Construimos el mensaje de registro
    gmess.bind('foaf', FOAF)
    gmess.bind('dso', DSO)
    reg_obj = agn[agentname+'-Register']
    gmess.add((reg_obj, RDF.type, DSO.Register))
    gmess.add((reg_obj, DSO.Uri, agn_uri))
    gmess.add((reg_obj, FOAF.Name, Literal(agentname)))
    gmess.add((reg_obj, DSO.Address, Literal(agn_addr)))
    gmess.add((reg_obj, DSO.AgentType, DSO.HotelsAgent))

    # Lo metemos en un envoltorio FIPA-ACL y lo enviamos
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
    return 'Nothing to see here'

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
    Simplementet retorna un objeto fijo que representa una
    respuesta a una busqueda de hotel

    Asumimos que se reciben siempre acciones que se refieren a lo que puede hacer
    el agente (buscar con ciertas restricciones, reservar)
    Las acciones se mandan siempre con un Request
    Prodriamos resolver las busquedas usando una performativa de Query-ref
    """
    global dsgraph
    global mss_cnt

    #Extraemos el mensaje y creamos un grafo con el
    message= request.args['content']
    gm = Graph()
    gm.parse(data=message)

    print gm.serialize(format='turtle')
    msgdic = get_message_properties(gm)

    # Comprobamos que sea un mensaje FIPA ACL
    if not msgdic is None:
        # Si no es, respondemos que no hemos entendido el mensaje
        gr = build_message(Graph(), ACL['not-understood'], sender= agn_uri, msgcnt=mss_cnt)
    else:
        # Obtenemos la performativa
        perf = msgdic['performative']

        if perf != ACL.request:
            # Si no es un request, respondemos que no hemos entendido el mensaje
            gr = build_message(Graph(), ACL['not-understood'], sender= agn_uri, msgcnt=mss_cnt)
        else:
            #Extraemos el objeto del contenido que ha de ser una accion de la ontologia de acciones del agente
            # de registro
            content = msgdic['content']

            # Averiguamos el tipo de la accion
            accion = gm.value(subject= content, predicate= RDF.type)

            # Aqui realizariamos lo que pide la accion
            # Por ahora simplemente retornamos un Inform-done
            gr = build_message(Graph(), ACL['inform-done'],
                               sender= agn_uri, msgcnt=mss_cnt,
                                       receiver=agn_uri,)
    mss_cnt += 1
    return gr


def tidyup():
    """
    Acciones previas a parar el agente

    """
    global cola1
    cola1.put(0)


def agentbehavior1(cola):
    """
    Un comportamiento del agente

    :return:
    """
    # Registramos el agente
    gr = register_message()
    print gr.serialize(format='turtle')

    # Escuchando la cola hasta que llegue un 0
    fin = False
    while not fin:
        while cola.empty():
            pass
        v = cola.get()
        if v == 0:
            fin = True
        else:
            print v

    # Selfdestruct
    requests.get(self_stop)

if __name__ == '__main__':
    # Ponemos en marcha los behaviors
    ab1=Process(target=agentbehavior1,args=(cola1,))
    ab1.start()

    # Ponemos en marcha el servidor
    app.run(host=hostname, port=port)

    # Esperamos a que acaben los behaviors
    ab1.join()
    print 'The End'
