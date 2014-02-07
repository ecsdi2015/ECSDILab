__author__ = 'javier'

import csv

ifile = open('airlines-clean.csv', "rb")
airlines = csv.reader(ifile)

ifile = open('airports-clean.csv', "rb")
airports = csv.reader(ifile)

ifile = open('routes.csv', "rb")
routes = csv.reader(ifile)

airline_s = {}
airport_s = {}

for i in airlines:
    airline_s[i[0]] = i[1]

for i in airports:
    airport_s[i[0]] = i[1]

ofile  = open('FlightData/routes-clean.csv', "wb")
writer = csv.writer(ofile, delimiter=',', quotechar='"')

for r in routes:
    if r[1] in airline_s and r[3] in airport_s and r[5] in airport_s:
        writer.writerow((airline_s[r[1]], airport_s[r[3]], airport_s[r[5]]))

ofile.close()



