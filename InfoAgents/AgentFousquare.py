__author__ = 'javier'

import foursquare

CLIENT_ID = '3NR1OSZ1OHVLP3P3U0OQPH2X2G4TBP3XABZ1LWDAB2UJV154'
CLIENT_SECRET = '5EEKPDPIGPWPJORULPGECQZCP5F5EIIXCY5YN25NH5QIBJWF'

client = foursquare.Foursquare(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)



v = client.venues.search(params={'ll':'41.4,2.14','intent':'browse','radius':'4000','query':'museo'})

print len(v['venues'])

for vn in v['venues']:
    print vn['name'],
    if len(vn['categories'])!=0:
        print vn['categories'][0]['name']

