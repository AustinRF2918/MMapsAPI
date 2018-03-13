"""Defines a MockDao which given a schema automatically generates Daos we can use."""

import uuid

from errors.error_types import ResourceNotFoundException
from util.schema_tools import is_matching_schema


class MockDao:
    def __init__(self, resource_schema):
        self.db_state = [resource_schema.get("example")]
        self.resource_schema = resource_schema

    def get_all(self):
        return self.db_state

    def get_item(self, el_id):
        matches = list(filter(lambda el: el["id"] == el_id, self.db_state))

        if matches:
            return matches[0]
        else:
            raise ResourceNotFoundException(self.resource_schema.get("name"), el_id)

    def add_item(self, el):
        is_matching_schema(el, self.resource_schema)

        el["id"] = str(uuid.uuid4())
        el["hash"] = hash(repr(el))

        self.db_state.append(el)

        return el

    def update_item(self, el_id, el):
        # TODO: implement this method.
        old_el = self.get_item(el_id)

        # Method merge_on_fields(fields, old_pin, new_pin)

        # new_pin = merge_on_fields(pin_putable_fields, old_pin, pin)

        # If company is present...
        # new_pin = merge_on_fields(pin_putable_fields, new_pin, pin.get("company"))


        # Write to db.

        return el

    def delete_item(self, el_id):
        matches = list(filter(lambda el: el["id"] == el_id, self.db_state))

        if matches:
            popped = matches[0]
            self.db_state.remove(popped)
            return popped
        else:
            raise ResourceNotFoundException(self.resource_schema.get("name"), el_id)
