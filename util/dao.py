"""Defines a MockDao which given a schema automatically generates Daos we can use."""

import uuid

from bson import ObjectId
from bson.errors import InvalidId
from pymongo import MongoClient

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

class MongoDao:
    def __init__(self, resource_schema, db_url, db_port):
        self.db = MongoClient(db_url, db_port)["tripout"][resource_schema.get("name")]
        self.resource_schema = resource_schema

    def get_all(self):
        return list(self.db.find({}))

    def get_item(self, el_id):
        match = self.db.find_one({"_id": ObjectId(el_id)})

        if match:
            return match
        else:
            raise ResourceNotFoundException(self.resource_schema.get("name"), el_id)

    def add_item(self, el):
        is_matching_schema(el, self.resource_schema)

        del el["_id"]
        el["revision"] = 1

        result = self.db.insert_one(el)
        return self.get_item(result.inserted_id)

    def update_item(self, el_id, el):
        old_el = self.get_item(el_id)

        del old_el["_id"]
        old_el["revision"] = old_el["revision"] + 1

        merged_el = merge_with_schema(old_el, el, self.resource_schema)

        self.db.replace_one({"_id": ObjectId(el_id)}, merged_el)

        return self.get_item(el_id)

    def delete_item(self, el_id):
        try:
            match = self.get_item(el_id)
            self.db.delete_one({"_id": ObjectId(el_id)})
            return match
        except InvalidId:
            raise ResourceNotFoundException(self.resource_schema.get("name"), el_id)

