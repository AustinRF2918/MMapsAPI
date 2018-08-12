"""Defines Pin resource."""
from flask import request
from flask_restful import Resource

from schema.pin import pin_request_schema, pin_pointer_schema, pin_response_schema
from util.dao import MongoDao
from util.schema_tools import marshal_with_schema

from tools.migrate import translate_to_old

pin_dao = MongoDao(pin_request_schema, "localhost", 27017)


class PinList(Resource):
    def get(self):
        return pin_dao.get_all()

    def post(self):
        pin = request.get_json(force=True)
        return pin_dao.add_item(pin)

class PinListLegacy(Resource):
    def get(self):
        return list(map(translate_to_old, pin_dao.get_all()))

class PinRevisionList(Resource):
    def get(self):
        return pin_dao.get_all()


class Pin(Resource):
    """Domain object for Michigan Maps pin. More docs to go here."""

    def get(self, id):
        return pin_dao.get_item(id)

    def delete(self, id):
        return pin_dao.delete_item(id)

    def patch(self, id):
        new_fields = request.get_json(force=True)
        return pin_dao.update_item(id, new_fields)
