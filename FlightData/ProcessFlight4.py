# -*- coding: utf-8 -*-
"""
File: ProcessFlight4

Created on 06/02/2014 15:58 

@author: bejar

"""
__author__ = 'bejar'


import csv

from SPARQLWrapper import SPARQLWrapper, JSON

from SPARQLPoints import OPENLINK, DBPEDIA


sparql = SPARQLWrapper(DBPEDIA)


ifile = open('DBAirports.csv', "rb")
airports = csv.reader(ifile)

query1=  """Prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
 Prefix ogc: <http://www.opengis.net/ont/geosparql#>
 Prefix geom: <http://geovocab.org/geometry#>
 Prefix lgdo: <http://linkedgeodata.org/ontology/>
 Prefix dbp: <http://dbpedia.org/ontology/>

Select *
   WHERE
  {"""

query2="""
      dbp:populationTotal ?t .
     }
  LIMIT 200
 """

ofile  = open('DBAirports-pop.csv', "wb")
writer = csv.writer(ofile, delimiter=',', quotechar='"')

for v in airports:
    try:
        queryt=query1+' <'+v[3]+'> '+query2
        sparql.setQuery(queryt)
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        pop = results['results']['bindings'][0]['t']['value']
        if int(pop) > 50000:
            print v[3],pop
            writer.writerow(v)
    except Exception:
        pass

ofile.close()


