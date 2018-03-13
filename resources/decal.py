"""Defines the Decal resource."""

from flask import request
from flask_restful import Resource, marshal_with

from schema.decal import decal_schema
from util.schema_tools import fieldize_schema
from util.dao import MockDao

mock_decal_dao = MockDao(decal_schema)


class DecalList(Resource):
    @marshal_with(fieldize_schema(decal_schema))
    def get(self):
        return mock_decal_dao.get_all()

    @marshal_with(fieldize_schema(decal_schema))
    def post(self):
        decal = request.get_json(force=True)
        return mock_decal_dao.add_item(decal)


class Decal(Resource):
    """Domain object for Michigan Maps pin. More docs to go here."""
    @marshal_with(fieldize_schema(decal_schema))
    def get(self, id):
        return mock_decal_dao.get_item(id)

    @marshal_with(fieldize_schema(decal_schema))
    def delete(self, id):
        return mock_decal_dao.delete_item(id)

