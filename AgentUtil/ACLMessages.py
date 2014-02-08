# -*- coding: utf-8 -*-
"""
filename: ACLMessages

Utilidades para tratar los mensajes FIPA ACL

Created on 08/02/2014

@author: javier
"""

__author__ = 'javier'

from rdflib import Graph
import requests
from rdflib.namespace import RDF
from OntoNamespaces import ACL, DSO


def is_message(graph):
    """
    Retorna si es un mensaje FIPA ACL
    """
    return graph.triples( (None,  RDF.type, ACL.FipaAclMessage)) is not None

def get_performative(graph):
        return graph.triples( (None,  RDF.type, ACL.Speechact))[0]

def send_message(gmess, perf, address, sender= None, receiver= None,  content= None, msgcnt=0):
    """
    Envia un mensaje como una performativa FIPA acl
    Para cuando hay que usar request para el envio

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