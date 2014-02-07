# -*- coding: utf-8 -*-
"""
File:

Created on 31/01/2014 8:55

@author: bejar

"""
__author__ = 'javier'


import csv
ifile = open('airlines.csv', "rb")

airlines = csv.reader(ifile)

ifile = open('airports.csv', "rb")

airports = csv.reader(ifile)

ifile = open('routes.csv', "rb")

routes = csv.reader(ifile)

airprout = set()
airlrout = set()


for v in routes:
    airprout.add(v[3])
    airprout.add(v[5])
    airlrout.add(v[1])

print len(airlrout), len(airprout)


lairp = []
for ap in airports:
    if ap[0] in airprout:
        lairp.append(ap)

lairl = []
for al in airlines:
    if al[0] in airlrout:
        lairl.append(al)

ofile  = open('FlightData/airports-clean.csv', "wb")
writer = csv.writer(ofile, delimiter=',', quotechar='"')
for row in lairp:
    roww = []
    roww.append(row[0])
    roww.append(row[4])
    writer.writerow(roww)
ofile.close()

ofile  = open('FlightData/airlines-clean.csv', "wb")
writer = csv.writer(ofile, delimiter=',', quotechar='"')
for row in lairl:
    roww = []
    roww.append(row[0])
    roww.append(row[3])
    writer.writerow(roww)
ofile.close()
