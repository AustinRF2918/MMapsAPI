"""Defines a MockDao which given a schema automatically generates Daos we can use."""

import uuid

from errors.error_types import ResourceNotFoundException
from util.schema_tools import is_matching_schema, merge_with_schema


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

        # TODO: Replace with actual DB push
        self.db_state.append(el)

        return el

    def update_item(self, el_id, el):
        # TODO: Replace with actual DB GET
        old_el = self.get_item(el_id)
        merged_el = merge_with_schema(old_el, el, self.resource_schema)

        # TODO Replace with DB PUT
        self.delete_item(el_id)
        self.db_state.append(merged_el)

        # TODO Replace with DB GET
        return self.get_item(el_id)

    def delete_item(self, el_id):
        # TODO Replace with DB DELETE via ID
        matches = list(filter(lambda el: el["id"] == el_id, self.db_state))

        if matches:
            popped = matches[0]
            self.db_state.remove(popped)
            return popped
        else:
            raise ResourceNotFoundException(self.resource_schema.get("name"), el_id)
