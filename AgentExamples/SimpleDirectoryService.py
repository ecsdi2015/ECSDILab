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
from ACLMessages import build_message

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
dir_uri = agn.Directory

app = Flask(__name__)
mss_cnt = 0

cola1 = Queue() # Cola de comunicacion entre procesos

@app.route("/Register")
def register():
    """
    Entry point del agente que recibe los mensajes de registro
    La respuesta es enviada al retornar la funcion
    No hay necesidad de enviar el mensaje explicitamente

    Asumimos una version simplificada del protocolo FIPA-request
    en la que no enviamos el mesaje Agree cuando vamos a responder

    :return:
    """
    global dsgraph
    global mss_cnt

    #Extraemos el mensaje y creamos un grafo con el
    message= request.args['content']
    gm = Graph()
    gm.parse(data=message)

    print gm.serialize(format='turtle')

    # Comprobamos que sea un mensaje FIPA ACL
    msg = gm.value(predicate=RDF.type,object= ACL.FipaAclMessage)
    if msg is None:
        # Si no es, respondemos que no hemos entendido el mensaje
        gr = build_message(Graph(), ACL['not-understood'], sender= dir_uri, msgcnt=mss_cnt)
    else:
        # Obtenemos la performativa
        perf = gm.value(subject= msg,predicate= ACL.performative)
        if perf != ACL.request:
            # Si no es un request, respondemos que no hemos entendido el mensaje
            gr = build_message(Graph(), ACL['not-understood'], sender= dir_uri, msgcnt=mss_cnt)
        else:
            #Extraemos el objeto del contenido que ha de ser una accion de la ontologia
            # de registro
            content = gm.value(subject=msg, predicate= ACL.content)
            # Averiguamos el tipo de la accion
            accion = gm.value(subject= content, predicate= RDF.type)

            # Accion de registro
            if accion == DSO.Register:
                # Si la hay extraemos el nombre del agente (FOAF.Name), el URI del agente
                # su direccion y su tipo
                agn_add = gm.value(subject=content, predicate=DSO.Address)
                agn_name = gm.value(subject=content, predicate=FOAF.Name)
                agn_uri = gm.value(subject=content, predicate=DSO.Uri)
                agn_type = gm.value(subject=content, predicate=DSO.AgentType)

                # Añadimos la informacion en el grafo de registro vinculandola a la URI
                # del agente y registrandola como tipo FOAF.Agent
                dsgraph.add((agn_uri, RDF.type, FOAF.Agent))
                dsgraph.add((agn_uri, FOAF.name, agn_name))
                dsgraph.add((agn_uri, DSO.Address, agn_add))
                dsgraph.add((agn_uri, DSO.AgentType, agn_type))

                # Generamos un mensaje de respuesta
                gr = build_message(Graph(),ACL.confirm,sender=dir_uri,
                                   receiver=agn_uri,msgcnt=mss_cnt)
            # Accion de busqueda
            # Asumimos que hay una accion de busqueda que puede tener
            # diferentes parametros en funcion de si se busca un tipo de agente
            # o un agente concreto por URI o nombre
            # Podriamos resolver esto tambien con un query-ref y enviar un objeto de
            # registro con variables y constantes
            if accion == DSO.Search:
                # Solo consideramos cuando Search indica el tipo de agente
                # Buscamos una coincidencia exacta
                # Retornamos el primero de la lista de posibilidades
                agn_type = gm.value(subject=content, predicate=DSO.AgentType)
                agn_uri = gm.value(subject=content, predicate=DSO.Uri)
                rsearch = dsgraph.triples((None, DSO.AgentType, agn_type))
                if rsearch is not None:
                    agn_uri = rsearch.next()[0]
                    agn_add = dsgraph.value(subject=agn_uri, predicate=DSO.Address)
                    gr = Graph()
                    gr.bind('dso',DSO)
                    rsp_obj = agn['Directory-response']
                    gr.add((rsp_obj, DSO.Address, agn_add))
                    gr.add((rsp_obj, DSO.Uri, agn_uri))
                    gr = build_message(gr, ACL.inform, sender= dir_uri, msgcnt=mss_cnt,
                                       receiver=agn_uri, content=rsp_obj)
                else:
                    # Si no encontramos nada retornamos un inform sin contenido
                    gr = build_message(Graph(), ACL.inform, sender=dir_uri, msgcnt=mss_cnt)
            # No habia ninguna accion en el mensaje
            else:
                gr = build_message(Graph(), ACL['not-understood'], sender= dir_uri, msgcnt=mss_cnt)
    mss_cnt += 1
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
    cola1.put(0)
    #dsgraph.close()

def agentbehavior1(cola):
    """
    Behaviour que simplemente espera mensajes de una cola y los imprime
    hasta que llega un 0 a la cola
    """
    fin = False
    while not fin:
        while cola.empty():
            pass
        v = cola.get()
        if v == 0:
            fin = True
        else:
            print v

if __name__ == '__main__':
    # Ponemos en marcha los behaviours como procesos
    ab1=Process(target=agentbehavior1,args=(cola1,))
    ab1.start()

    # Ponemos en marcha el servidor Flask
    app.run(host= hostname, port= port, debug= True)

    # Cerramos los procesos
    ab1.terminate()

    print 'The End'

