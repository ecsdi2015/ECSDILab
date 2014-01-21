__author__ = 'bejar'

from SPARQLWrapper import SPARQLWrapper, JSON, TURTLE, XML
from rdflib import RDF, RDFS
sparql = SPARQLWrapper("http://lod2.openlinksw.com/sparql")
#sparql = SPARQLWrapper("http://dbpedia.org/sparql")
sparql = SPARQLWrapper("http://chandra.lsi.upc.edu:8890/sparql")

# sparql.setQuery("""
#     PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
#
#     SELECT  ?val,  ?label
#     WHERE { ?val  <http://yago-knowledge.org/resource/isConnectedTo>   <http://yago-knowledge.org/resource/Barcelona>.
#             ?val  <http://yago-knowledge.org/resource/isLocatedIn> ?label}
# """)

sparql.setQuery("""
SELECT  ?subj,  ?lit
WHERE { ?subj foaf:name ?lit}
""")

sparql.setReturnFormat(JSON)
results = sparql.query()
results.print_results()

print

# sparql = SPARQLWrapper("http://linkedgeodata.org/sparql")
#
# sparql.setQuery("""
# Prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
# Prefix ogc: <http://www.opengis.net/ont/geosparql#>
# Prefix geom: <http://geovocab.org/geometry#>
# Prefix lgdo: <http://linkedgeodata.org/ontology/>
#
# Select *
# From <http://linkedgeodata.org> {
#   ?s
#     a lgdo:Restaurant ;
#     rdfs:label ?l ;
#     geom:geometry [
#       ogc:asWKT ?g
#     ] .
#
#     Filter(bif:st_intersects (?g, bif:st_point (2.16, 41.4), 0.4)) .
# }
# """)
# sparql.setReturnFormat(JSON)
# results = sparql.query()
# print results.print_results()

# sparql.setQuery("""
# PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
# PREFIX dbpo: <http://dbpedia.org/property/>
# SELECT ?subdivision ?label
# WHERE {
#   <http://dbpedia.org/resource/Catalunya> dbpo:subdivisionName ?subdivision .
#   ?subdivision rdfs:label ?label .
# }
# """)
# sparql.setReturnFormat(JSON)
# results = sparql.query()
# results.print_results()