"""Tools for working with schema types."""
import copy
from flask_restful import fields


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

    is_matching_schema(merged_data, schema)

    return merged_data


def is_matching_schema(data, schema):
    required_fields = []
    schema_fields = schema.get("fields")

    for key, value in schema_fields.items():
        if value["required"]:
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
                    is_matching_schema(data[key], schema_fields.get(key).get("schema"))
                elif key_type == list and schema_fields.get(key).get("schema") is not None:
                    for element in data[key]:
                        is_matching_schema(element, schema_fields.get(key).get("schema"))