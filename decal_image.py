"""Defines the DecalImage DAO and data structure."""

from flask_restful import Resource, fields, marshal_with

decal_image_fields = {
    "id": fields.String,
    "url": fields.String
}

class DecalImageDao:
    """Data access object for a decal image. Will be connected to DB later on."""
    def __init__(self, id, url):
        self.id = id
        self.url = url

class DecalImage(Resource):
    """Domain object for Michigan Maps decal image. More docs to go here."""
    @marshal_with(decal_image_fields)
    def get(self, **kwargs):
        return DecalImageDao(id = "afdsafdsafdsa", url = "roflcoper.com")


