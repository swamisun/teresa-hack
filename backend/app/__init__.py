from __future__ import print_function
import os
import sys
import logging
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

from flask import Flask, Blueprint, request
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api
from twilio.rest import Client
from twilio.twiml.messaging_response import MessagingResponse

from config import app_config


db = SQLAlchemy()

PREFIX = "/api/v1.0"

twilio_client = Client()

def create_app(config_name):
    app = Flask(__name__, instance_relative_config=True)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.from_object(app_config[config_name])
    app.config.from_pyfile('config.py')
    db.init_app(app)

    # error logger
    handler = TimedRotatingFileHandler('log/teresa', when='midnight', backupCount=7)
    handler.setLevel(logging.INFO)
    app.logger.addHandler(handler)

    # access logger
    logger = logging.getLogger('werkzeug')
    handler = logging.FileHandler('access.log')
    logger.addHandler(handler)
    app.logger.addHandler(handler)

    blueprint = Blueprint('tree', __name__)

    api = Api(blueprint, prefix=PREFIX)
    from views import ResourceEndpoint, CustomerEndpoint, TwilioEndpoint
    api.add_resource(ResourceEndpoint, '/resources')
    api.add_resource(CustomerEndpoint, '/customers')
    @app.route('/api/v1.0/twilio', methods=['GET'])
    def twilio():
        if request.method == 'GET':
            message = TwilioEndpoint(request.args)
            response = MessagingResponse()
            response.message('Hi ' + message )
            return str(response), 200, {'Content-Type': 'application/xml'}

    app.register_blueprint(blueprint)

    print ("*** Starting up at {} ***".format(datetime.now()))

    return app
