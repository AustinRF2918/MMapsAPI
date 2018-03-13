"""Tools for working with schema types."""
from flask_restful import fields


def fieldize_schema(schema):
    schema_fields = schema.get("fields")
    fieldized_map = {}

    for key, value in schema_fields.items():
        fieldized_map[key] = value.get("type")

    return fieldized_map


validation_mapping = {
    fields.String: str,
    fields.Nested: dict,
    fields.List: list,
    fields.Integer: int,
    fields.Float: float,
}


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
            key_type = validation_mapping.get(schema_fields.get(key).get("type"))
            if key_type == None:
                key_type = validation_mapping.get(type(schema_fields.get(key).get("type")))

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