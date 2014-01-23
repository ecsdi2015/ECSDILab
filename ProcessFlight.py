__author__ = 'javier'


import csv
ifile  = open('/home/javier/airlines.csv', "rb")

reader = csv.reader(ifile)

i=0
for v in reader:
    if v[7] == 'Y' and v[3]!='':
        print v[1],v[3],v[6]
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
