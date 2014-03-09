import json

import requests

import config

API_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
DEFAULT_PARAMS = dict(sensor='false', key=config.google_api_key)

def nearby_places(lat, lng, radius=100):
    params = dict(DEFAULT_PARAMS)
    params['location'] = '{},{}'.format(lat, lng)
    params['radius'] = radius
    response = requests.get(API_URL, params=params)
    return json.loads(response.text)['results']


if __name__ == '__main__':
    for place in nearby_places(45.767, 4.833):
        for key, value in place.iteritems():
            print key, '->', value
        print '-'*80
        print
