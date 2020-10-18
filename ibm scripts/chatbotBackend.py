import sys
import requests
from cloudant.client import Cloudant


import subprocess
# import sys
import config
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install('geopy')
install('googlemaps')

from geopy.geocoders import Nominatim
import googlemaps
from googlemaps import places


def getUserAddress():
    client = Cloudant.iam("d02a0070-4a25-4e81-b712-a8e6c38a8863-bluemix", "0CpvlhxnS58tIZMsdu4QuUqw4bai6t1EYcJAv4Mo4lnI")
    client.connect()
    database_name = "user_db"
    # print(client.all_dbs())
    db = client[database_name] #open database
    print(db)
    userDoc = db["user1"]
    print(userDoc)
    return userDoc['userData']['address']

# print(getUserAddress())


def find_closest_foodbank(address):
    geolocator = Nominatim(user_agent="foodBankLocator")
    location = geolocator.geocode(address)
    coordinates = (location.latitude, location.longitude)
    client = googlemaps.Client(key=config.googleKey)
    nearby_banks = places.places_nearby(client=client, location=coordinates, radius=24140, keyword='food bank')
    food_bank_list = []
    for foodbank in nearby_banks['results']:
        location_coord = foodbank['geometry']['location']['lat'], foodbank['geometry']['location']['lng']
        address = geolocator.reverse(str(location_coord[0]) + ", " + str(location_coord[1]))
        food_bank_list.append(foodbank['name'])
    print(food_bank_list)
    return food_bank_list

def getBankInfo():
    client = Cloudant.iam("d02a0070-4a25-4e81-b712-a8e6c38a8863-bluemix", "0CpvlhxnS58tIZMsdu4QuUqw4bai6t1EYcJAv4Mo4lnI")
    client.connect()
    database_name = "user_db"
    # print(client.all_dbs())
    db = client[database_name] #open database
    # print(db)
    userDoc = db["user1"]
    return userDoc['userData']['accountInformation']

def main(dict):
    if dict['type'] == 'investment':
        ## do stuff with rohits code
        print('hello')
    elif dict['type'] == 'food_bank':
        print('hello')
        address = getUserAddress()
        list = find_closest_foodbank(address)
        return {'output' : list}
    elif dict['type'] == 'bank_info':
        return getBankInfo()
    elif dict['type'] == 'billing':
        ## edit billing or display current billing
        print('hello')
    elif dict['type'] == 'budget':
        ##do stuff with budget, return, change ...
        print('budget')

# main({'type' : 'food_bank'})
