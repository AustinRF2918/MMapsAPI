"""Defines Pin resource."""
from flask import request
from flask_restful import Resource, marshal_with

from schema.pin import pin_schema, pin_reduced_schema
from util.schema_tools import fieldize_schema
from util.dao import MongoDao

mock_pin_dao = MongoDao(pin_schema, "localhost", 27017)


class PinList(Resource):
    @marshal_with(fieldize_schema(pin_schema))
    def get(self):
        return mock_pin_dao.get_all()

    @marshal_with(fieldize_schema(pin_schema))
    def post(self):
        pin = request.get_json(force=True)
        return mock_pin_dao.add_item(pin)


class PinHashList(Resource):
    @marshal_with(fieldize_schema(pin_reduced_schema))
    def get(self):
        return mock_pin_dao.get_all()


class Pin(Resource):
    """Domain object for Michigan Maps pin. More docs to go here."""

    @marshal_with(fieldize_schema(pin_schema))
    def get(self, id):
        return mock_pin_dao.get_item(id)

    @marshal_with(fieldize_schema(pin_schema))
    def delete(self, id):
        return mock_pin_dao.delete_item(id)

    @marshal_with(fieldize_schema(pin_schema))
    def patch(self, id):
        new_fields = request.get_json(force=True)
        return mock_pin_dao.update_item(id, new_fields)