# -*- coding: utf-8 -*-
"""
File: ProcessFlight5

Created on 07/02/2014 7:34 

@author: bejar

"""

__author__ = 'bejar'


import csv
from rdflib import Graph
from OntoNamespaces import TIO

ifile = open('Routes-DBpedia.csv', "rb")
routes = csv.reader(ifile)

ofile  = open('routes-DBpedia.csv', "wb")

routesg = Graph()

for ro in routes:



