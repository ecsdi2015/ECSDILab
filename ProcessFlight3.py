__author__ = 'javier'

__author__ = 'javier'

import csv

ifile = open('FlightData/DBAirlines.csv', "rb")
airlines = csv.reader(ifile)

ifile = open('FlightData/DBAirports.csv', "rb")
airports = csv.reader(ifile)

ifile = open('FlightData/routes-clean.csv', "rb")
routes = csv.reader(ifile)

airline_s = {}
airport_s = {}

for i in airlines:
    airline_s[i[2]] = i[0]

for i in airports:
    airport_s[i[2]] = (i[0], i[-2], i[-1])

ofile  = open('FlightData/routes-DBpedia.csv', "wb")
writer = csv.writer(ofile, delimiter=',', quotechar='"')
for r in routes:
    if r[0] in airline_s and r[1] in airport_s and r[2] in airport_s:
        writer.writerow((airline_s[r[0]],
                         airport_s[r[1]][0],
                         airport_s[r[1]][1],
                         airport_s[r[1]][2],
                         airport_s[r[2]][0],
                         airport_s[r[2]][1],
                         airport_s[r[2]][2]))

ofile.close()
