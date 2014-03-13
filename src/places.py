import json
from pprint import pprint

import requests

import config

API_URL = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
PHOTO_URL = 'https://maps.googleapis.com/maps/api/place/photo?sensor={sensor}&key={key}&photoreference={photoreference}&maxheight={maxheight}&maxwidth={maxwidth}'
DEFAULT_PARAMS = dict(sensor='false', key=config.google_api_key)

def nearby_places(lat, lng, radius=100):
    params = dict(DEFAULT_PARAMS)
    params['location'] = '{},{}'.format(lat, lng)
    params['radius'] = radius
    response = requests.get(API_URL, params=params)
    data = json.loads(response.text)['results']
    for p_data in data:
        if 'photos' in p_data:
            photo_params = dict(DEFAULT_PARAMS)
            photo_params.update(dict(photoreference=p_data['photos'][0]['photo_reference'], maxheight=400, maxwidth=700))
            p_data['main_photo'] = PHOTO_URL.format(**photo_params)

    return data

if __name__ == '__main__':
    for place in nearby_places(45.767, 4.833):
        pprint(place)
        print '-'*80
        print
