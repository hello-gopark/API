from flask import Flask
import requests
import re
import collections
from flask import Flask, render_template, request, jsonify, make_response
import ipaddress
import ast

collections.Iterable = collections.abc.Iterable
  
location1 = {'latitude': 22.302923233819364,'longitude': 114.16795742516831}

app = Flask(_name_)

@app.route('/', methods=['GET'])
def geolocation():
  ip = request.remote_addr
  print(ip)
  eq = requests.get('https://ipgeolocation.abstractapi.com/v1/?ip_address=' + ip + '&api_key=780db2980b4045a0bc74c6c9dba995ca')
  return make_response(jsonify(eq.json()))



@app.route("/<location>", methods=['GET'])
def getmaps(location=location1):
  slot_dicts = {}
  mins = {}
  
  location = ast.literal_eval(location)
  
  latitude = location['latitude']
  longitude = location['longitude']

  url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json?location=" + str(latitude) + "%2C"+ str(longitude) + "&radius=5000&type=parking&key=AIzaSyBozURAd7-HF5T6aTuvxRERMdDNAaB98mA"

  payload={}
  headers = {}

  response = requests.request("GET", url, headers=headers, data=payload)

  for slot in response.json()['results']:
    slot_dicts[slot['name']] = {'latitude':slot['geometry']['location']['lat'], 'longitude':slot['geometry']['location']['lng'], 'name':slot['name']}

  for slot in slot_dicts.values():
    url1 = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=" + str(latitude) + "%2C" + str(longitude) + "&destinations=" + str(slot['latitude']) + "%2C" + str(slot['longitude']) + "&key=AIzaSyBozURAd7-HF5T6aTuvxRERMdDNAaB98mA"

    payload1={}
    headers1 = {}

    response1 = requests.request("GET", url1, headers=headers1, data=payload1)

    tup = (('latitude', slot['latitude']), ('longitude', slot['longitude']), ('name', slot['name']))

    mins[tup] = int(re.findall('\d+', response1.json()['rows'][0]['elements'][0]['duration']['text'])[0])

  sorted_mins = dict(sorted(mins.items(), key=lambda x:x[1], reverse = False))
  sorted_mins

  listed_mins = list(sorted_mins.items())

  # marker_locations = []

  # for slot in slot_dicts.values():
  #   marker_locations.append((slot['latitude'], slot['longitude']))

  # gmaps.configure(api_key='AIzaSyBozURAd7-HF5T6aTuvxRERMdDNAaB98mA')

  # origin = (location_cords['latitude'], location_cords['longitude'])
  # destination = (listed_mins[0][0][0][1], listed_mins[0][0][1][1])

  # fig = gmaps.figure()

  # layer = gmaps.directions.Directions(origin, destination, mode='car')

  # fig.add_layer(layer)

  # markers = gmaps.marker_layer(marker_locations)

  # fig.add_layer(markers)
  
  return jsonify({'latitude':(listed_mins[0][0][0][1] + 100), 'longitude':(listed_mins[0][0][1][1]+100)})

if _name_ == "_main_":
    app.run(host="127.0.0.1", port=8080, debug=True)