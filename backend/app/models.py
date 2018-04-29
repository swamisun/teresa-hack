# local modules
from app import db


class Resources(db.Model):
    """
    Create a Resources model
    """

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(45), nullable=False)
    category = db.Column(db.String(45), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    zip_code = db.Column(db.String(10))
    quantity = db.Column(db.Integer)
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    timestamp = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    description = db.Column(db.String(255))
    image_url = db.Column(db.String(255), nullable=False)
    url = db.Column(db.String(255), nullable=False)
    min_age = db.Column(db.Integer)
    max_age = db.Column(db.Integer)
    gender = db.Column(db.CHAR(1))
    accessibility = db.Column(db.String(45))

    def __init__(self, name, category, address, zip_code, quantity,
                 start_time, end_time, description, image_url,
                 url, min_age, max_age, gender, accessibility, timestamp=""):
        self.name = name
        self.category = category
        self.address = address
        self.zip_code = zip_code
        self.quantity = quantity
        self.start_time = start_time
        self.end_time = end_time
        if timestamp is not "":
            self.timestamp = timestamp
        self.description = description
        self.image_url = image_url
        self.url = url
        self.min_age = min_age
        self.max_age = max_age
        self.gender = gender
        self.accessibility = accessibility

    def __repr__(self):
        return '{{ "resource_id": "{}",' \
               ' "name": "{}",' \
               '  "category": "{}",' \
               '  "address": "{}",' \
               '  "zip_code": "{}",' \
               '  "quantity": {},' \
               '  "start_time": "{}",' \
               '  "end_time": "{}",' \
               '  "timestamp": "{}",' \
               '  "description": "{}",' \
               '  "image_url": "{}",' \
               '  "url": "{}",' \
               '  "min_age": {},' \
               '  "max_age": {},' \
               '  "gender": "{}",' \
               '  "accessibility": "{}" }}'.format(self.id, self.name, self.category, self.address,
                                                   self.zip_code, self.quantity, self.start_time,
                                                   self.end_time, self.timestamp, self.description,
                                                   self.image_url, self.url, self.min_age, self.max_age,
                                                   self.gender, self.accessibility)


class Customers(db.Model):
    """
    Create a Customers model
    """

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    phone = db.Column(db.String(45), nullable=False)
    latitude = db.Column(db.String(45), nullable=False)
    longitude = db.Column(db.String(45), nullable=False)
    age = db.Column(db.Integer)
    gender = db.Column(db.CHAR(1))
    family_size = db.Column(db.Integer)

    def __init__(self, phone, latitude, longitude,
                 age, gender, family_size=1):
        self.phone = phone
        self.latitude = latitude
        self.longitude = longitude
        self.age = age
        self.gender = gender
        self.family_size = family_size

    def __repr__(self):
        return '{{ "customer_id": "{}",' \
               ' "phone": "{}",' \
               '  "latitude": "{}",' \
               '  "longitude": "{}",' \
               '  "age": {},' \
               '  "gender": "{}",' \
               '  "family_size": {} }}'.format(self.id, self.phone, self.latitude, self.longitude,
                                               self.age, self.gender, self.family_size)
