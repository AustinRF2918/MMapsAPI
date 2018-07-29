"""Defines the Decal resource."""

from flask import request
from flask_restful import Resource

from schema.decal import decal_schema
from util.schema_tools import marshal_with_schema
from util.dao import MongoDao

decal_dao = MongoDao(decal_schema, "localhost", 27017)


class DecalList(Resource):
    def get(self):
        return decal_dao.get_all()

    def post(self):
        decal = request.get_json(force=True)
        return decal_dao.add_item(decal)


class Decal(Resource):
    """Domain object for Michigan Maps pin. More docs to go here."""
    def get(self, id):
        return decal_dao.get_item(id)

    def delete(self, id):
        return decal_dao.delete_item(id)

