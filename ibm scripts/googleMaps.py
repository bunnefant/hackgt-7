import requests
from config import *
key = googleKey
print(key)

url = 'https://maps.googleapis.com/maps/api/place/findplacefromtext/json?input=food%20bank&inputtype=textquery&fields=formatted_address,name,opening_hours&locationbias=point:33.77,-84.39&key='

r = requests.get(url + key)
print(r.json())
