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


def build_message(gmess, perf, sender= None, receiver= None,  content= None, msgcnt= 0):
    """
    Envia un mensaje como una performativa FIPA acl
    Asume que en el grafo que se recibe esta ya el contenido y esta ligado al
    URI en el parametro contenido
    Para cuando hay que usar request para el envio

    :param gmess:
    :return:
    """
    # Añade los elementos del speechact al grafo del mensaje
    mssid = 'message-'+str(sender.__hash__()) + '-{:{fill}4d}'.format(msgcnt, fill='0')
    ms = ACL[mssid]
    gmess.bind('acl', ACL)
    gmess.add((ms, RDF.type, ACL.FipaAclMessage))
    gmess.add((ms, ACL.performative, perf))
    gmess.add((ms, ACL.sender, sender))
    if receiver is not None:
        gmess.add((ms, ACL.receiver, receiver))
    if content is not None:
        gmess.add((ms, ACL.content, content))
    return gmess

def send_message(gmess, address):
    """

    """
    msg = gmess.serialize(format='xml')
    r = requests.get(address, params={'content': msg})

    # Procesa la respuesta y la retorna como resultado como grafo
    gr = Graph()
    gr.parse(data=r.text)

    return gr

