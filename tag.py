"""Defines the Tag DAO and data structure."""

from flask_restful import Resource, fields, marshal_with

# The following is fields on the tag db structure that
# we will publically expose.
tag_fields = {
    "id": fields.String
}

class TagDao:
    """Data access object for a tag . Will be connected to DB later on."""
    def __init__(self, id):
        self.id = id

class Tag(Resource):
    """Domain object for Michigan Maps pin. More docs to go here."""
    @marshal_with(tag_fields)
    def get(self, **kwargs):
        return TagDao(id = "afdsafdsafdsa")

