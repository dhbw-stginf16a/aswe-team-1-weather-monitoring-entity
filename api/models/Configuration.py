#!/usr/bin/env python3

import logging

import os

class Config:
    def __init__(self):
        self.CENTRAL_NODE_BASE_URL = os.environ.setdefault('CENTRAL_NODE_BASE_URL', 'http://localhost:8080/api/v1')
        self.OUR_URL = os.environ.setdefault('OWN_URL', 'http://localhost:5000')
        self.readApiToken = False
        self.apiToken = None

    def getAPItoken(self):
        if not self.readApiToken:
            try:
                from api.models.prefstore import PREFSTORE_CLIENT
                self.apiToken = PREFSTORE_CLIENT.get_global_pref()['weather_api_token']
                self.readApiToken = True
            except:
                self.readApiToken = True
                raise BaseException("Failed to read API Token")
        return self.apiToken



CONFIG = Config()