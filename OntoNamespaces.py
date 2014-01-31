# -*- coding: utf-8 -*-
"""
File: OntoNamespaces

Created on 31/01/2014 8:55

Diversos namespaces utiles y algunas clases y propiedades de esos namespaces

@author: bejar

"""

__author__ = 'bejar'


from rdflib import Graph, RDF, RDFS, OWL, Namespace, Literal

# FIPA ACL Ontology
ACL = Namespace("http://www.nuin.org/ontology/fipa/acl#")

speechact = ACL.SpeechAct

# OWL- S Ontology

OWLSService = Namespace('http://www.daml.org/services/owl-s/1.2/Service.owl#')
OWLSProfile = Namespace('http://www.daml.org/services/owl-s/1.2/Profile.owl#')


