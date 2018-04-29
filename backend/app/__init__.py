from datetime import datetime
import logging
from logging.handlers import TimedRotatingFileHandler

from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Resource, Api

from config import app_config


db = SQLAlchemy()

PREFIX = "/api/v1.0"


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
    from views import ResourceEndpoint, CustomerEndpoint
    api.add_resource(ResourceEndpoint, '/resources')
    api.add_resource(CustomerEndpoint, '/customers')

    app.register_blueprint(blueprint)

    print ("*** Starting up at {} ***".format(datetime.now()))

    return app
