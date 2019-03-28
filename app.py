#!/usr/bin/env python3

import logging

import connexion
from flask_cors import CORS
from api.models.RegistrationThread import RegistrationThread
from api.models.Configuration import CONFIG


logger = logging.getLogger(__name__)

app = connexion.App(__name__, specification_dir='openapi/')
app.add_api('openapi.yml')

# Set CORS headers
CORS(app.app)

# set the WSGI application callable to allow using uWSGI:
# uwsgi --http :8080 -w app
application = app.app

logger.info('App initialized')

app.registerThread = RegistrationThread(CONFIG.CENTRAL_NODE_BASE_URL, CONFIG.OUR_URL)
app.registerThread.start()
