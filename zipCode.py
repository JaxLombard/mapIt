import googlemaps
from datetime import datetime
from mapit import address

gmaps = googlemaps.Client(key='')
geocode_result = gmaps.geocode(address)
zipcode = details['Locality']['PostalCode']['PostCodeNumber']
print(zipcode)