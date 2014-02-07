# -*- coding: utf-8 -*-
"""
File: ProcessFlight5

Created on 07/02/2014 7:34 

@author: bejar

"""

__author__ = 'bejar'


import csv
from rdflib import Graph, Namespace, URIRef, Literal
from OntoNamespaces import TIO, RDF
from random import randint

ifile = open('routes-DBpedia-all.csv', "rb")
routes = csv.reader(ifile)

routesg = Graph()

for ro in routes:
    flno = ro[1]+str(randint(1000,9000))
    uriflno = URIRef('http://Flights.org/'+flno)
    routesg.add((uriflno, RDF.type, TIO.Flight))
    routesg.add((uriflno, TIO.flightNo, Literal(flno)))
    routesg.add((uriflno, TIO['from'],URIRef(ro[2])))
    routesg.add((uriflno, TIO['to'],URIRef(ro[5])))
    routesg.add((uriflno, TIO['operatedBy'],URIRef(ro[0])))



routesg.bind('tio', TIO)
routesg.bind('rdf', RDF)


ofile  = open('routes-DBpedia-all.ttl', "wb")
routesg.serialize(destination=ofile, format='turtle')