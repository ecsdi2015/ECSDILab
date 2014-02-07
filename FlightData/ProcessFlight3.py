__author__ = 'javier'

import csv

ifile = open('DBAirlines.csv', "rb")
airlines = csv.reader(ifile)

ifile = open('DBAirports-pop.csv', "rb")
airports = csv.reader(ifile)

ifile = open('routes-clean.csv', "rb")
routes = csv.reader(ifile)

airline_s = {}
airport_s = {}

for i in airlines:
    airline_s[i[2]] = (i[0],i[2])

for i in airports:
    airport_s[i[2]] = (i[0], i[-2], i[-1])

ofile  = open('routes-DBpedia.csv', "wb")
writer = csv.writer(ofile, delimiter=',', quotechar='"')
for r in routes:
    if r[0] in airline_s and r[1] in airport_s and r[2] in airport_s:
        writer.writerow((airline_s[r[0]][0],
                         airline_s[r[0]][1],
                         airport_s[r[1]][0],
                         airport_s[r[1]][1],
                         airport_s[r[1]][2],
                         airport_s[r[2]][0],
                         airport_s[r[2]][1],
                         airport_s[r[2]][2]))

ofile.close()
