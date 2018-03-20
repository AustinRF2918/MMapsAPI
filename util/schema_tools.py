"""Tools for working with schema types."""
import copy

from apispec import APISpec
from flask_restful import fields, marshal_with

# Global mutation
api_specification = APISpec(
    title="Michigan Maps API",
    version="1.0.0",
    info={
        "description": "API for Michigan Maps mobile application and dashboard application"
    }
)

# Data definitions
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


# Utility methods.
def validate_schema(schema: dict):
    """Validates a schema matches schema of a schema throws if invalid!."""

    assert type(schema.get("name")) is str
    assert type(schema.get("fields")) is dict
    schema_fields = schema["fields"]
    for key, value in schema_fields.items():
        assert type(value) is dict
        assert type(value.get("type")) is not None
        assert type(value.get("required")) is bool
        assert type(value.get("read_only")) is bool
        assert type(value.get("description")) is str
    assert type(schema.get("example")) is dict


def fieldize_schema(schema: dict) -> dict:
    """Returns Flask marshallable field map. Use with @marsh_with"""

    validate_schema(schema)

    schema_fields = schema.get("fields")
    fieldized_map = {}

    for key, value in schema_fields.items():
        fieldized_map[key] = value.get("type")

    return fieldized_map


def get_required_request_fields(schema: dict) -> frozenset:
    """Gets all required fields in the request for a given schema."""

    validate_schema(schema)

    required_fields = set()
    for key, value in schema.get("fields").items():
        if value["required"] and not value["read_only"]:
            required_fields.add(key)

    return frozenset(required_fields)


def get_request_fields(schema: dict) -> frozenset:
    """Gets all fields that may be sent in request for a given schema."""

    validate_schema(schema)

    writeable_fields = set()
    for key, value in schema.get("fields").items():
        if not value["read_only"]:
            writeable_fields.add(key)

    return frozenset(writeable_fields)


def deduce_field_mapping(value: any) -> type:
    """Given any type (preferably defined in Flask fields) deduces original Python mapping."""

    try:
        # Case 1: value is defined as pointer to function.
        item_type = flask_to_py_mapping[value.get("type")]
    except KeyError:
        # Case 2: value is defined as instantiated generic.
        item_type = flask_to_py_mapping[type(value.get("type"))]
    except:
        # Case 3: value is not mapped!
        raise KeyError("No mapping was present for " + value.get("type"))

    return item_type


def merge_with_schema(old_data: dict, new_data: dict, schema: dict) -> dict:
    """Given an old data and a new data, uses a schema to perform a semantic merge."""
    validate_schema(schema)

    writeable_fields = get_request_fields(schema)

    merged_data = copy.deepcopy(old_data)

    for field in writeable_fields:
        if field in new_data.keys():
            merged_data[field] = new_data[field]

    validate_data_to_schema(merged_data, schema)

    return merged_data


def validate_data_to_schema(data: dict, schema: dict):
    """Determines if data matches a schema or not."""
    validate_schema(schema)

    required_fields = get_required_request_fields(schema)
    schema_fields = schema.get("fields")

    # Presence checking
    for field in required_fields:
        if data.get(field) is None:
            raise TypeError("Field {} on schema {} was required but not present!".format(
                field,
                schema.get("name")
            ))

    # Type checking
    for key, value in data.items():
        if schema_fields.get(key) is not None:
            key_type = deduce_field_mapping(schema_fields.get(key))

            if key_type is not None and not isinstance(value, key_type):
                # Case 1: Key type doesn't coorespond to actual type.
                raise TypeError("Key {} on schema {} was expected to be of type {} but was {}.".format(
                    key,
                    schema.get("name"),
                    key_type,
                    type(value)
                ))
            else:
                # Case 2: It does, but it is also a nested type
                item_schema = schema_fields.get(key).get("schema")

                if key_type == dict and item_schema is not None:
                    # Case 2a: Field is dict and has a schema
                    validate_data_to_schema(value, item_schema)
                elif key_type == list and item_schema is not None:
                    # Case 2b: Field is list and has nested schema.
                    for element in value:
                        validate_data_to_schema(element, item_schema)


class marshal_with_schema(object):
    """Wraps standard flask marshaller to use our own."""

    def __init__(self, schema, envelope=None):
        self.marshaller = marshal_with(fieldize_schema(schema), envelope=envelope)

    def __call__(self, f):
        return self.marshaller.__call__(f)


# User defined global mutation
def register_schema(schema: dict) -> dict:
    """Registers a schema in the global swagger spec and performs validation on schemas."""

    validate_schema(schema)
    schema_fields, name, example = schema.get("fields"), schema.get("name"), schema.get("example")
    validate_data_to_schema(example, schema)

    mapped_fields = {}

    for key, value in schema_fields.items():
        item_type = deduce_field_mapping(value)

        if value.get("schema"):
            schema_reference = "#/definitions/" + value.get("schema")["name"]

            if item_type is list:
                # Case 1: List of ->Object.
                mapped_fields[key] = {
                    "type": "array",
                    "items": {
                        "$ref": schema_reference
                    }
                }
            else:
                # Case 2: ->Object
                mapped_fields[key] = {
                    "$ref": schema_reference
                }
        else:
            if item_type is list:
                # Case 3: List of Primitive
                list_type = type(value.get("type").container)

                mapped_fields[key] = {
                    "type": py_to_swagger_mapping[item_type],
                    "items": {
                        "type": py_to_swagger_mapping[flask_to_py_mapping[list_type]]
                    }
                }
            else:
                # Case 4: Primitive
                mapped_fields[key] = {
                    "type": py_to_swagger_mapping[item_type],
                }

    api_specification.definition(name, properties=mapped_fields)
    print("Successfully registered schema: {}".format(name))

    return schema


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
