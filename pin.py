"""Defines the Pin DAO and data structure."""
import uuid

from flask import request
from flask_restful import Resource, fields, marshal_with

from mock import mock_pins_db
from common import MissingFieldException, ResourceNotFoundException

# Company fields data structure that is directly used
# by the Pin structure.
company_fields = {
    "title": fields.String,
    "message": fields.String,
    "is_featured": fields.Boolean,
    "photo_stream": fields.List(fields.String)
}

required_company_fields = ["title", "message", "is_featured"]

# The following is fields on the pin db structure that
# we will publicly expose.
pin_fields = {
    # Base Metadata
    "id": fields.String,
    "hash": fields.String,

    # Core Domain Data
    "phone_number": fields.String,
    "description": fields.String,
    "address": fields.String,
    "image": fields.String,
    "company_data": fields.Nested(company_fields),

    # Tagging Metadata
    "tags": fields.List(fields.String),

    # Locational Metadata
    "latitude": fields.Float,
    "longitude": fields.Float,

    # Link Metadata
    "logo_image_link": fields.String,
    "social_links": fields.List(fields.String),
    "website_link": fields.String,
}

required_pin_fields = ["address", "latitude", "longitude", "description"]

# Reduced pin fields to only include id and hash. For our /pins/hash endpoint.
pin_fields_reduced = {
    # Base Metadata
    "id": fields.String,
    "hash": fields.String,
}

def validate_conforming_types(data, schema, required_fields=[]):
    validation_mapping = {
        fields.String: str,
        fields.Nested: dict,
        fields.List: list,
        fields.Integer: int,
        fields.Float: float,
    }

    for field in required_fields:
        if data.get(field) is None:
            raise MissingFieldException(field)

    for key, value in data.items():
        if schema.get(key) is not None:
            if not isinstance(value, validation_mapping.get(schema.get(key))):
                # TODO Give better error
                raise TypeError("Key {} was of invalid type!".format(key))



class PinDao:
    """Data access object for a pin . Will be connected to DB later on."""
    def __init__(self, config):
        self.config = config

        # TODO: Make this rely on real db instead of managing it at runtime!
        self.db_state = mock_pins_db

    def get_pins(self, with_fields=None):
        if not with_fields:
            return self.db_state
        else:
            # TODO: Optimization for DB: Allow specification of what fields are to be queried.
            # This will help deserializer if we have huge data set.
            return self.db_state

    def get_pin(self, pin_id):
        matches = list(filter(lambda pin: pin["id"] == pin_id, self.db_state))
        return matches[0] if matches else None

    def add_pin(self, pin):
        validate_conforming_types(pin, pin_fields, required_pin_fields)

        if pin.get("company_data") is not None:
            validate_conforming_types(pin.get("company_data"), company_fields, required_company_fields)

        pin["id"] = uuid.uuid4()
        pin["hash"] = hash(repr(pin))
        self.db_state.append(pin)

        return pin

class PinList(Resource):
    def __init__(self):
        self.pin_dao = PinDao({})

    @marshal_with(pin_fields)
    def get(self):
        return self.pin_dao.get_pins()

    @marshal_with(pin_fields)
    def post(self):
        pin = request.get_json(force=True)
        return self.pin_dao.add_pin(pin)

class PinHashList(Resource):
    def __init__(self):
        self.pin_dao = PinDao({})

    @marshal_with(pin_fields_reduced)
    def get(self):
        return self.pin_dao.get_pins(with_fields=["id", "hash"])

class Pin(Resource):
    def __init__(self):
        self.pin_dao = PinDao({})

    """Domain object for Michigan Maps pin. More docs to go here."""
    @marshal_with(pin_fields)
    def get(self, id, **kwargs):
        result = self.pin_dao.get_pin(id)

        if result:
            return result
        else:
            raise ResourceNotFoundException("pin", id)

    # TODO: Implement delete


