import json

with open('venues_data.json', 'r') as v:
    venues = json.load(v)
    outlets = venues['outlets']

    length = len(outlets)
    print(length)
