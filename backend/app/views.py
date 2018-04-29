from __future__ import print_function
import sys
from datetime import time

from sqlalchemy import exc
from flask_restful import Resource, Api, fields, marshal_with
from flask import abort, request


from app import db
from models import Resources, Customers
from gmaps import GoogleMaps


FOOD = ['hungry', 'food', 'eat', 'soup', 'kitchen']
FOOD_INTENT = 'food'
SHELTER = ['room', 'sleep', 'board', 'shelter']
SHELTER_INTENT = 'shelter'
NEARBY = 5.0  # 5 miles

gmaps = GoogleMaps()


def get_intent(message):
    if any(food_intent in message for food_intent in FOOD):
        return FOOD_INTENT
    if any(shelter_intent in message for shelter_intent in SHELTER):
        return SHELTER_INTENT


def store_user_info(user_phone, user_zip):
    (lat, lng) = gmaps.get_lat_long(address=user_zip)
    customer = Customers(phone=user_phone, latitude=lat,
                         longitude=lng, age=18, gender='')
    print("*** customer object generated:", customer, file=sys.stderr)
    try:
        db.session.add(customer)
        db.session.commit()
        print("*** Added customer:", str(customer), file=sys.stderr)
    except exc.IntegrityError:
        db.session().rollback()
        print("Potential duplicate entry")


def get_resources_for_user(user_intent, user_zip):
    resources = Resources.query.filter_by(category=user_intent)
    print("*** {} resources available:".format(len(resources)), file=sys.stderr)
    nearby_resources = [res for res in resources if (gmaps.calculate_distance(res.address, user_zip) < NEARBY)]
    print("*** {} nearby resources available:".format(len(nearby_resources)), file=sys.stderr)
    return nearby_resources


def TwilioEndpoint(args):
    user_phone = args.get('From', '')
    user_zip = args.get('FromZip', '94086')
    message = args.get('Body', 'No message!')
    print("*** SMS received: {} from {} @ {}".format(message, user_phone, user_zip), file=sys.stderr)
    store_user_info(user_phone, user_zip)
    user_intent = get_intent(message)
    print("*** User intent:", user_intent, file=sys.stderr)
    # user = Customers.query.filter_by(phone=user_phone)
    nearby_resources = get_resources_for_user(user_intent, user_zip)
    message = 'Sorry! No nearby resource for {} found'.format(user_intent)
    if len(nearby_resources)>0:
        resource = nearby_resources[0]
        print("*** Nearest resource:", resource, file=sys.stderr)
        message = 'Great news! {} has {} available between {} to {}'.format(resource.name, user_intent,
                                                                            resource.start_time, resource.end_time)
    return message


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
        for resource in resources:
            try:
                print("**** resource:", resource, file=sys.stderr)
            except:
                print ("####### Failed to print ID:", resource.id, file=sys.stderr)
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


class CustomerEndpoint(Resource):
    customer_fields = {
        "id": fields.String,
        "phone": fields.String,
        "latitude": fields.String,
        "longitude": fields.String,
        "age": fields.Integer,
        "gender": fields.String,
        "family_size": fields.Integer}

    @marshal_with(customer_fields)
    def get(self):
        customers = Customers.query.all()
        for customer in customers:
            try:
                print("**** customer:", customer, file=sys.stderr)
            except:
                print ("####### Failed to print ID:", customer.id, file=sys.stderr)
        return customers, 200, {'Content-Type': 'application/json'}

    @marshal_with(customer_fields)
    def post(self):
        customer = Customers(phone=request.json.get('phone', ''),
                             latitude=request.json.get('latitude', ''),
                             longitude=request.json.get('longitude', ''),
                             age=request.json.get('age', 99),
                             gender=request.json.get('gender', ''),
                             family_size=request.json.get('family_size', ''))
        print("*** customer object generated:", customer, file=sys.stderr)
        try:
            db.session.add(customer)
            db.session.commit()
            print("*** Added customer:", str(customer), file=sys.stderr)
            return customer, 201, {'Content-Type': 'application/json'}
        except exc.IntegrityError:
            db.session().rollback()
            return "Potential duplicate entry", 409, {'Content-Type': 'application/json'}
