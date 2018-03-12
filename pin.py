"""Defines the Pin DAO and data structure."""

from flask_restful import Resource, fields, marshal_with, marshal

from mock import mock_pins_db

# Company fields data structure that is directly used
# by the Pin structure.
company_fields = {
    "title": fields.String,
    "message": fields.String,
    "is_featured": fields.Boolean,
    "photo_stream": fields.List(fields.String)
}

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

class PinDao:
    """Data access object for a pin . Will be connected to DB later on."""
    def __init__(self, config):
        self.config = config

    def get_pins(self):
        return mock_pins_db


class PinList(Resource):
    def __init__(self):
        self.pin_dao = PinDao({})

    @marshal_with(pin_fields)
    def get(self):
        return self.pin_dao.get_pins()

class Pin(Resource):
    """Domain object for Michigan Maps pin. More docs to go here."""
    @marshal_with(pin_fields)
    def get(self, **kwargs):
        return PinDao(id = "afdsafdsafdsa")

