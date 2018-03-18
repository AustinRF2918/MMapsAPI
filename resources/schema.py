"""Allows one to get OpenAPI 2 formatted schema definitions (Specifically for Swagger-UI)"""
from flask_restful import Resource

from util.schema_tools import api_specification

class Schema(Resource):
    def get(self):
        return api_specification.to_dict()