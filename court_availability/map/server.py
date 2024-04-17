import json
import flask

from flask import Flask


app = Flask(__name__)


@app.route("/", methods=['GET'])
def display_map():

    date = None

    with open('venues_data.json', 'r') as f:
        venues_data = json.load(f)

    location_ids = []

    with open('courts_25_04_2024.json', 'r') as f:
        data = json.load(f)

        date = data['date']

        for court in data['available_courts']:
            id = court['id']

            location_ids.append(id)

    found_locations = []

    for location_id in location_ids:

        location_data = {}

        venue_match = None

        for venue in venues_data['outlets']:
            if venue['id'] == location_id:
                venue_match = venue

        if venue_match is None:
            continue

        lat_value = venue_match['lat']
        lng_value = venue_match['lng']

        if int(lat_value) == 0 or int(lng_value) == 0:
            continue

        location_data['id'] = location_id
        location_data['label'] = venue_match['label']
        location_data['lat'] = lat_value
        location_data['lng'] = lng_value

        found_locations.append(location_data)

    response = flask.jsonify(
        {"date": date,
         "found_locations": found_locations
         })

    response.headers.add('Access-Control-Allow-Origin', '*')

    return response
