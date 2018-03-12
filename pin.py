"""Defines the Pin DAO and data structure."""

from flask_restful import Resource, fields, marshal_with

# Company fields data structure that is directly used
# by the Pin structure.
company_fields = {
    "title": fields.String,
    "message": fields.String
    "is_featured": fields.Boolean,
    "photo_stream": fields.List(fields.Url)
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
    "image": fields.Url,
    "company_data": fields.Nested(company_fields),

    # Tagging Metadata
    "tags": fields.List(fields.String),

    # Locational Metadata
    "latitude": fields.Float,
    "longitude": fields.Float,

    # Link Metadata
    "logo_image_link": fields.Url,
    "social_links": fields.List(fields.Url),
    "website_link": fields.Url,
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

