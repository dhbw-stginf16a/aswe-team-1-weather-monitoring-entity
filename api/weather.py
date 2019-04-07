#!/usr/bin/env python3

import logging
import json

import requests
import re
import datetime
from api.models.Configuration import CONFIG

logger = logging.getLogger(__name__)

def requestFromLocation(location, endpoint, params = None, apiToken=None):
    # Analyse what has to be queried q or zip
    if params is None:
        params = dict()
    if apiToken is None:
        apiToken = CONFIG.getAPItoken()
    assert type(params) is dict
    params['appid'] = apiToken
    params['units'] = "metric"
    zipCode = re.compile("\d*,.*")
    if zipCode.fullmatch(location):
        params['zip'] = location
    else:
        params['q'] = location

    url = "https://api.openweathermap.org/data/2.5/" + endpoint
    return requests.get(url, params)

def requestForecast(location, time):
    requestedTime = datetime.datetime.utcfromtimestamp(time)
    assert requestedTime > datetime.datetime.utcnow()
    data = json.loads(requestFromLocation(location, 'forecast').text)
    for item in reversed(data['list']):
        if requestedTime > datetime.datetime.utcfromtimestamp(int(item['dt'])):
            return item
    return data['list'][0]

def getCurrentWeather(body):
    try:
        location = body['payload']['location']
        data = ""
        if body['type'] == 'weather_current':
            data = json.loads(requestFromLocation(location, 'weather').text)
        elif body['type'] == 'weather_forecast':
            time = body['payload']['time']
            data = requestForecast(location, int(time))
        else:
            logger.error("Unknown request type: " + body['type'])
            return {"error":"Unknown request type: " + body['type']}, 404

        response = {
            'type': body['type'],
            'payload': {
                'data': data
            }
        }

        return [response], 200
    except BaseException as e:
        logger.error("An error occurred: " + str(e))
        return {"error":"Internal server error: " + str(e)}, 500
