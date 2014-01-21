__author__ = 'javier'


import requests
import pprint
KEY = 'bstjr2k73t9pmqtm8mggmehe'
CID = '55505 '

EAN_END_POINT = 'http://api.ean.com/ean-services/rs/hotel/v3/list'

# r = requests.get(EAN_END_POINT,
#                  params={'apiKey': KEY, 'cid': CID, 'numberOfResults': 5, 'city': 'Barcelona', 'countryCode': 'es'})
#

r = requests.get(EAN_END_POINT,
                 params={'apiKey': KEY, 'cid': CID, 'numberOfResults': 5,
                         'latitude': '041.40000', 'longitude': '002.16000',
                         'searchRadius': 2, 'searchRadiusUnit': 'KM',
                         'arrivalDate': '01/30/2014', 'departureDate': '02/05/2014'
                 })

dic = r.json()
for hot in dic['HotelListResponse']['HotelList']['HotelSummary']:
    print hot['name']

