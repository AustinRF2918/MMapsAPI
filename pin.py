"""Defines the Pin DAO and data structure."""

from flask_restful import Resource, fields, marshal_with

# The following is fields on the pin db structure that
# we will publically expose.
pin_fields = {
    "id": fields.String,
    "description": fields.String,
    "address": fields.String,
    "image": fields.String, # This is a URL.
    "hash": fields.String,
    "image": fields.String,
    "phone_number": fields.String,

    "latitude": fields.Float,
    "longitude": fields.Float,

    "social_links": fields.List,
    "website_link": fields.String
}

class PinDao:
    """Data access object for a pin . Will be connected to DB later on."""
    def __init__(self, id):
        self.id = id

class Pin(Resource):
    """Domain object for Michigan Maps pin. More docs to go here."""
    @marshal_with(pin_fields)
    def get(self, **kwargs):
        return PinDao(id = "afdsafdsafdsa")

