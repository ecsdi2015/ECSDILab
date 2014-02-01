__author__ = 'javier'


import csv
ifile = open('/home/javier/airlines.csv', "rb")

airlines = csv.reader(ifile)

i=0
for v in airlines:
    if v[7] == 'Y' and v[3]!='':
        #print v[1],v[3],v[6]
        i += 1

print i

ifile = open('/home/javier/airports.csv', "rb")

airports = csv.reader(ifile)

i=0
for v in airports:
    if v[4] != '' and v[4] != '\N' and v[5] != '' and v[5] != '\N':
        #print v[1],v[4],v[5]
        i += 1


print i


# ofile  = open('/home/javier/airports2.csv', "wb")

# writer = csv.writer(ofile, delimiter=',', quotechar='"')
#
# for row in reader:
#     writer.writerow(row)
#
#
# ifile.close()
# ofile.close()
