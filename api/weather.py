#!/usr/bin/env python3

import logging
import json

import requests
import re
from api.models.Configuration import CONFIG

logger = logging.getLogger(__name__)

def requestFromLocation(location, endpoint, params = None, apiToken=CONFIG.getAPItoken()):
    # Analyse what has to be queried q or zip
    if params is None:
        params = dict()
    if type(params) is not dict:
        raise BaseException("Expect dictionary for params")
    params['appid'] = apiToken
    params['units'] = "metric"
    zipCode = re.compile("\d*,.*")
    if zipCode.fullmatch(location):
        params['zip'] = location
    else:
        params['q'] = location

    url = "https://api.openweathermap.org/data/2.5/" + endpoint
    return requests.get(url, params)

def getCurrentWeather(body):
    location = body['payload']['location']
    if not body['type'] == 'weather_current':
        logger.debug("Unknown request type: " + body['type'])
        raise BaseException("Unknown request type")

    data = requestFromLocation(location, 'weather')

    response = {
        'type': body['type'],
        'payload': {
            'data': json.loads(data.text)
        }
    }

    return [response], 200
