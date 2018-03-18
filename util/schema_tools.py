"""Tools for working with schema types."""
import copy
from functools import wraps

from apispec import APISpec
from flask_restful import fields, marshal_with


def fieldize_schema(schema):
    schema_fields = schema.get("fields")
    fieldized_map = {}

    for key, value in schema_fields.items():
        fieldized_map[key] = value.get("type")

    return fieldized_map


flask_to_py_mapping = {
    fields.String: str,
    fields.Nested: dict,
    fields.List: list,
    fields.Integer: int,
    fields.Float: float,
    fields.Boolean: bool,
}

py_to_swagger_mapping = {
    str: "string",
    dict: "object",
    list: "array",
    int: "integer",
    float: "number",
    bool: "boolean"
}


def merge_with_schema(old_data, new_data, schema):
    writeable_fields = []
    schema_fields = schema.get("fields")

    for key, value in schema_fields.items():
        if not value["read_only"]:
            writeable_fields.append(key)

    merged_data = copy.deepcopy(old_data)

    for field in writeable_fields:
        if field in new_data.keys():
            merged_data[field] = new_data[field]

    return merged_data


def is_matching_request_schema(data, schema):
    required_fields = []
    schema_fields = schema.get("fields")

    for key, value in schema_fields.items():
        if value["required"] and not value["read_only"]:
            required_fields.append(key)

    for field in required_fields:
        if data.get(field) is None:
            raise TypeError("Field {} on schema {} was required but not present!".format(
                field,
                schema.get("name")
            ))

    for key, value in data.items():
        if schema_fields.get(key) is not None:
            key_type = flask_to_py_mapping.get(schema_fields.get(key).get("type"))
            if key_type == None:
                key_type = flask_to_py_mapping.get(type(schema_fields.get(key).get("type")))

            if key_type is not None and not isinstance(value, key_type):
                raise TypeError("Key {} on schema {} was expected to be of type {}.".format(
                    key,
                    schema.get("name"),
                    key_type
                ))
            else:
                if key_type == dict and schema_fields.get(key).get("schema") is not None:
                    is_matching_request_schema(data[key], schema_fields.get(key).get("schema"))
                elif key_type == list and schema_fields.get(key).get("schema") is not None:
                    for element in data[key]:
                        is_matching_request_schema(element, schema_fields.get(key).get("schema"))

api_specification = APISpec(
    title = "Michigan Maps API",
    version = "1.0.0",
    info = {
        "description": "API for Michigan Maps mobile application and dashboard application"
    }
)


def register_schema(schema):
    """Registers a schema in the global swagger spec and performs validation on schemas."""

    schema_fields, name, example = validate_schema(schema)
    is_matching_request_schema(schema.get("example"), schema)

    mapped_fields = {}

    for key, value in schema_fields.items():
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
    return schema



def validate_schema(schema):
    """Validates a schema matches schema of a schema."""
    assert type(schema.get("name")) is str
    name = schema["name"]
    assert type(schema.get("fields")) is dict
    schema_fields = schema["fields"]
    for key, value in schema_fields.items():
        assert type(value) is dict
        assert type(value.get("type")) is not None
        assert type(value.get("required")) is bool
        assert type(value.get("read_only")) is bool
        assert type(value.get("description")) is str
    assert type(schema.get("example")) is dict
    example = schema["example"]
    return schema_fields, name, example


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
                    },
                    "examples": {
                        "application/json": [value.get("schema").get("example")]
                    }
                }
            else:
                transformed_schema_mapping[key] = {
                    "description": description,
                    "content": {
                        "application/json": {
                            "schema": {
                                "$ref": "#/definitions/" + value.get("schema").get("name")
                            },
                        }
                    },
                    "examples": {
                        "application/json": value.get("schema").get("example")
                    }
                }

    if method == "post" or method == "patch" or method == "put":
        if request_type:
            parameters = [{
                    "in": "body",
                    "name": request_type,
                    "schema": {
                        "$ref": "#/definitions/" + request_type
                }
            }]

        else:
            parameters = [{
                    "in": "body",
                    "name": tag,
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


class marshal_with_schema(object):
    """Wraps standard flask marshaller to use our own."""

    def __init__(self, schema, envelope=None):
        self.marshaller = marshal_with(fieldize_schema(schema))

    def __call__(self, f):
        return self.marshaller.__call__(f)
