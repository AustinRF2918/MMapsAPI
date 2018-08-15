"""Allows one to get OpenAPI 2 formatted schema definitions (Specifically for Swagger-UI)"""
from flask_restful import Resource
from flask_httpauth import HTTPBasicAuth

from util.schema_tools import api_specification
from util.auth import auth

class Schema(Resource):
    def get(self):
        return api_specification.to_dict()

    @auth.login_required
    def post(self):
        return "Good"
