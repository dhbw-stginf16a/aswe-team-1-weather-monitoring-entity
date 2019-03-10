#!/usr/bin/env python3

import logging
import json

from api.models.prefstore import getAPItoken
import requests

logger = logging.getLogger(__name__)

def requestFromLocation(location, url, params = "", apiToken=getAPItoken()):
    # Analyse what has to be queried q or zip
    return requests.get("http://" + url + '?q=' + location + '&APPID=' + apiToken + (("&" + params) if params != "" else ""))

def getCurrentWeather(body):
    location = body['payload']['location']
    if not body['type'] == 'weather_current':
        logger.debug("Unknown request type: " + body['type'])
        raise BaseException("Unknown request type")

    data = requestFromLocation(location, 'api.openweathermap.org/data/2.5/weather')

    response = {
        'type': body['type'],
        'payload': {
            'data': json.loads(data.text)
        }
    }

    return [response], 200
