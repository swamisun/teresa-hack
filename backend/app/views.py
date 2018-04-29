from __future__ import print_function
import sys
from datetime import time

from sqlalchemy import exc
from flask_restful import Resource, Api, fields, marshal_with
from flask import abort, request


from app import db
from models import Resources


class ResourceEndpoint(Resource):
    resource_fields = {
        "id": fields.String,
        "name": fields.String,
        "category": fields.String,
        "address": fields.String,
        "zip_code": fields.String,
        "quantity": fields.Integer,
        "start_time": fields.String,
        "end_time": fields.String,
        "timestamp": fields.DateTime,
        "description": fields.String,
        "image_url": fields.String,
        "url": fields.String,
        "min_age": fields.Integer,
        "max_age": fields.Integer,
        "gender": fields.String,
        "accessibility": fields.String}

    @marshal_with(resource_fields)
    def get(self):
        resources = Resources.query.all()
        print("**** resources:", str(resources), file=sys.stderr)
        return resources, 200, {'Content-Type': 'application/json'}

    @marshal_with(resource_fields)
    def post(self):
        resource = Resources(name=request.json.get('name', ''),
                             category=request.json.get('category', ''),
                             address=request.json.get('address', ''),
                             zip_code=request.json.get('zip_code', ''),
                             quantity=request.json.get('quantity', ''),
                             start_time=request.json.get('start_time', time(hour=00, minute=00)),
                             end_time=request.json.get('end_time', time(hour=00, minute=00)),
                             timestamp=request.json.get('timestamp', ),
                             description=request.json.get('description', ''),
                             image_url=request.json.get('image_url', ''),
                             url=request.json.get('url', ''),
                             min_age=request.json.get('min_age', 0),
                             max_age=request.json.get('max_age', 99),
                             gender=request.json.get('gender', ''),
                             accessibility=request.json.get('accessibility', ''))
        print("*** resource object generated:", resource, file=sys.stderr)
        try:
            db.session.add(resource)
            db.session.commit()
            print("*** Added resource:", str(resource), file=sys.stderr)
            return resource, 201, {'Content-Type': 'application/json'}
        except exc.IntegrityError:
            db.session().rollback()
            return "Potential duplicate entry", 409, {'Content-Type': 'application/json'}