# -*- coding: utf-8 -*-
"""
Created on Fri Dec 27 15:58:13 2013

Agente que realiza peticiones

Demo de agente que utiliza las performativas FIPA para comunicación entre agentes
Las performativas estan definidas en la ontologia fipa-acl.owl

@author: javier
"""

__author__ = 'javier'

import requests
from rdflib import Namespace, URIRef, Graph, ConjunctiveGraph, Literal
from rdflib.namespace import FOAF, RDF
from rdflib.plugins.memory import IOMemory
from OntoNamespaces import ACL
import socket

# Configuration stuff
hostname = socket.gethostname()
port = 9001

agn = Namespace("http;//www.agentes.org#")
gm = Graph()


ms = ACL['message0000']
gm.bind('acl',ACL)
gm.bind('foaf',FOAF)

gm.add((ms, RDF.type, ACL.SpeechAct))
gm.add((ms, ACL.performative, ACL.request))
gm.add((agn.pepe, FOAF.name, Literal('Pepe')))
gm.add((ms, ACL.sender, agn.pepe))

msg = gm.serialize(format='xml')
r=requests.get('http://chandra.lsi.upc.edu:8890/agente',params={'content':msg})

gr =Graph()
gr.parse(data=r.text)

print gr.serialize(format='turtle')
