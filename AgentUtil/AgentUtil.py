# -*- coding: utf-8 -*-
"""
File: AgentUtil

Created on 31/01/2014 9:31

Diferentes funciones comunes a los agentes implementados en ECSDI

@author: bejar

"""

__author__ = 'bejar'

from flask import request
from rdflib import Graph
import requests
from rdflib.namespace import RDF

from OntoNamespaces import ACL


def shutdown_server():
    """
    Funcion que para el servidor web

    :raise RuntimeError:
    """
    func = request.environ.get('werkzeug.server.shutdown')
    if func is None:
        raise RuntimeError('Not running with the Werkzeug Server')
    func()

def send_message(gmess, perf, address, sender= None, receiver= None,  content= None, msgcnt=0):
    """
    Envia un mensaje como una performativa FIPA acl

    :param gmess:
    :return:
    """
    # Añade los elementos del speechact al grafo del mensaje
    ms = ACL['message{:{fill}4d}'.format(msgcnt, fill='0')]
    gmess.bind('acl', ACL)
    gmess.add((ms, RDF.type, ACL.SpeechAct))
    gmess.add((ms, ACL.performative, perf))
    gmess.add((ms, ACL.sender, sender))

    msg = gmess.serialize(format='xml')
    r = requests.get(address, params={'content': msg})

    # Procesa la respuesta y la retorna como resultado
    gr = Graph()
    gr.parse(data=r.text)

    return gr
