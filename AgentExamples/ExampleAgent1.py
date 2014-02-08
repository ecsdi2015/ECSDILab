# -*- coding: utf-8 -*-
"""
filename: ExampleAgent1

Agente que se registra, busca en el registro un agente y le envia un mensaje

Created on 08/02/2014

@author: javier
"""

__author__ = 'javier'


from  multiprocessing import Process
import socket

from flask import Flask, render_template, request, url_for
from rdflib import Graph, Namespace, Literal, URIRef
from rdflib.namespace import FOAF, RDF
import requests

from OntoNamespaces import ACL, OWLSProfile, OWLSService
from AgentUtil import shutdown_server, send_message