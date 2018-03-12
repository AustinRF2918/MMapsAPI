'''Defines the Pin DAO and data structure.'''

from flask_restful import Resource, fields, marshal_with

pin_fields = {
    "id": fields.String
}

class PinDao:
    def __init__(self, id):
        self.id = id

class Pin(Resource):
    """Domain object for Michigan Maps pin. More docs to go here."""
    @marshal_with(pin_fields)
    def get(self, **kwargs):
        return PinDao(id = "afdsafdsafdsa")

