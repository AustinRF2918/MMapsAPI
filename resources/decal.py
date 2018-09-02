"""Defines the Decal resource."""

from flask import request
from flask_restful import Resource
from flask_httpauth import HTTPBasicAuth

from schema.decal import decal_schema
from util.schema_tools import marshal_with_schema
from util.dao import MongoDao
from util.auth import auth

decal_dao = MongoDao(decal_schema, "mongodb://localhost", 27017)

class DecalList(Resource):
    def get(self):
        return decal_dao.get_all()

    @auth.login_required
    def post(self):
        decal = request.get_json(force=True)
        return decal_dao.add_item(decal)


class Decal(Resource):
    def get(self, id):
        return decal_dao.get_item(id)

    @auth.login_required
    def delete(self, id):
        return decal_dao.delete_item(id)

