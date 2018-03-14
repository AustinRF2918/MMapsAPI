"""Allows one to get OpenAPI 2 formatted schema definitions (Specifically for Swagger-UI)"""
from flask_restful import Resource
from apispec import APISpec

from util.schema_tools import flask_to_py_mapping, py_to_swagger_mapping

api_specification = APISpec(
    title = "Michigan Maps API",
    version = "1.0.0",
    info = {
        "description": "API for Michigan Maps mobile application and dashboard application"
    }
)

def add_api_schema(schema):
    name = schema["name"]
    fields = schema["fields"]

    mapped_fields = {}

    for key, value in fields.items():
        try:
            item_type = flask_to_py_mapping[value.get("type")]
        except KeyError:
            item_type = flask_to_py_mapping[type(value.get("type"))]
        except:
            raise KeyError("No key found for type: " + value.get("type"))

        if value.get("schema"):
            if item_type is list:
                mapped_fields[key] = {
                    "type": "array",
                    "items": {
                        "$ref": "#/definitions/" + value.get("schema").get("name")
                    }
                }
            else:
                mapped_fields[key] = {
                    "$ref": "#/definitions/" + value.get("schema").get("name")
                }

        else:
            if item_type is list:
                mapped_fields[key] = {
                    "type": py_to_swagger_mapping[item_type],
                    "items": {
                        "type": py_to_swagger_mapping[flask_to_py_mapping[type(value.get("type").container)]]
                    }
                }
            else:
                mapped_fields[key] = {
                    "type": py_to_swagger_mapping[item_type],
                }

    api_specification.definition(name, properties=mapped_fields)

def register_resource(endpoint, tag, description, method, code_schema_mapping, request_type = None, qparams = []):
    transformed_schema_mapping = {}
    parameters = []


    for key, value in code_schema_mapping.items():
            if (value.get("array")):
                transformed_schema_mapping[key] = {
                    "description": description,
                    "content": {
                        "application/json": {
                            "schema": {
                                "type": "array",
                                "items": {
                                    "$ref": "#/definitions/" + value.get("schema").get("name")
                                }
                            }
                        }
                    }
                }
            else:
                transformed_schema_mapping[key] = {
                    "description": description,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/definitions/" + value.get("schema").get("name")
                            }
                        }
                    }
                }

    if method == "post" or method == "patch" or method == "put":
        if request_type:
            parameters = [{
                    "in": "body",
                    "name": request_type,
                    "description": "lol",
                    "schema": {
                        "$ref": "#/definitions/" + request_type
                }
            }]

        else:
            parameters = [{
                    "in": "body",
                    "name": tag,
                    "description": "lol",
                    "schema": {
                        "$ref": "#/definitions/" + tag
                    }
                }]

    for param in qparams:
        parameters.append({"in": "path", "name": param, "type": "string"})

    api_specification.add_path(
        path = endpoint,
        operations = {
            method: {
                "tags": [tag],
                "responses": transformed_schema_mapping,
                "parameters": parameters
            }
        }
    )

    print(api_specification.to_dict())



class Schema(Resource):
    def get(self):
        return api_specification.to_dict()
