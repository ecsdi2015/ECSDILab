# -*- coding: utf-8 -*-
"""
File: SimpleAgent

Created on 30/01/2014 11:32 

@author: bejar

"""

__author__ = 'bejar'

#from  multiprocessing import Process
#from flask import Flask,request
from rdflib import Graph, RDF, RDFS, OWL, Namespace, Literal, URIRef
from rdflib.namespace import FOAF, RDF
import requests



def sendmessage(gmess):
    global mss_cnt
    ms = acl['message{:{fill}4d}'.format(mss_cnt, fill='0')]
    mss_cnt +=1
    gmess.bind('acl', acl)
    gmess.bind('owlss', OWLSService)
    gmess.bind('owlsp', OWLSProfile)
    gmess.bind('foaf', FOAF)

    gmess.add((ms, RDF.type, acl.SpeechAct))
    gmess.add((ms, acl.performative, acl.request))
    gmess.add((servuri, FOAF.name, Literal(agentname)))
    gmess.add((ms, acl.sender, servuri))
    msg = gmess.serialize(format='xml')
    r = requests.get('http://chandra.lsi.upc.edu:8890/Register', params={'content': msg})

    gr = Graph()
    gr.parse(data=r.text)

    print gr.serialize(format='turtle')


mss_cnt = 0
agentname = 'Agente1'
OWLSService = Namespace('http://www.daml.org/services/owl-s/1.2/Service.owl#')
OWLSProfile = Namespace('http://www.daml.org/services/owl-s/1.2/Profile.owl#')
acl = Namespace("http://www.nuin.org/ontology/fipa/acl#")
agn = Namespace("http;//www.agentes.org#")

gm = Graph()

servuri = agn.Agente1
servuriprof = URIRef('http://agentes.com/agente1profile')

gm.add((servuri, RDF.type, OWLSService.Service))
gm.add((servuriprof, RDF.type, OWLSProfile.Profile))
gm.add((servuri, OWLSService.presents, servuriprof))
gm.add((servuri, OWLSProfile.serviceName, Literal(agentname)))

sendmessage(gm)
sendmessage(gm)
