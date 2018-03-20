"""Defines a MockDao which given a schema automatically generates Daos we can use."""

import uuid

import copy
from bson import ObjectId
from bson.errors import InvalidId
from pymongo import MongoClient

from errors.error_types import ResourceNotFoundException
from util.schema_tools import validate_data_to_schema, merge_with_schema, marshal_with_schema


class MongoDao:
    def __init__(self, resource_schema, db_url, db_port):
        self.db_url = db_url
        self.db_port = db_port
        self.schema_name = resource_schema.get("name")

        self.db = MongoClient(db_url, db_port)["tripout"][self.schema_name]
        self.resource_schema = resource_schema

    def get_all(self):
        def replace_id(item):
            item["_id"] = str(item["_id"])
            return item

        return list(map(self._render_pointers, map(replace_id, self.db.find({}))))

    def get_item(self, el_id):
        print("Getting item in " + self.schema_name)
        match = self.db.find_one({"_id": ObjectId(el_id)})

        if match:
            match["_id"] = str(match["_id"])
            return self._render_pointers(match)
        else:
            raise ResourceNotFoundException(self.resource_schema.get("name"), el_id)

    def add_item(self, el):
        print("Adding item in " + self.schema_name)

        del el["_id"]
        el["revision"] = 1

        # Validation
        validate_data_to_schema(el, self.resource_schema)
        self._validate_pointers(el)

        result = self.db.insert_one(el)
        return self.get_item(result.inserted_id)

    def update_item(self, el_id, el):
        print("Updating item in " + self.schema_name)

        old_el = self.get_item(el_id)

        del old_el["_id"]
        old_el["revision"] = old_el["revision"] + 1

        merged_el = merge_with_schema(old_el, el, self.resource_schema)

        # Validation
        validate_data_to_schema(merged_el, self.resource_schema)
        self._validate_pointers(merged_el)

        self.db.replace_one({"_id": ObjectId(el_id)}, merged_el)

        return self.get_item(el_id)

    def delete_item(self, el_id):
        print("Deleting item in " + self.schema_name)

        try:
            match = self.get_item(el_id)
            self.db.delete_one({"_id": ObjectId(el_id)})
            return match
        except InvalidId:
            raise ResourceNotFoundException(self.resource_schema.get("name"), el_id)


    def _validate_pointers(self, el):
        # Additional DAO level validation to make sure reduced schema exists in db!
        for key, value in self.resource_schema.get("fields").items():
            if value.get("schema") is not None and value.get("schema").get("pointer_to") is not None and el.get(key):
                resource_id = el.get(key).get("_id")
                resource_name = value.get("schema").get("pointer_to").get("name")

                # TODO Slow as hell. Use a map to cache dbs
                result_db = MongoClient(self.db_url, self.db_port)["tripout"][resource_name]
                cross_results = result_db.find_one({"_id": ObjectId(resource_id)})
                cross_results["_id"] = str(cross_results["_id"])

                if not cross_results:
                    raise ResourceNotFoundException(resource_name, resource_id)

    def _render_pointers(self, el):
        rendered_el = copy.deepcopy(el)
         # Additional DAO level validation to make sure reduced schema exists in db!
        for key, value in self.resource_schema.get("fields").items():
            if value.get("schema") is not None and value.get("schema").get("pointer_to") is not None and el.get(key):
                    resource_id = el.get(key).get("_id")
                    resource_name = value.get("schema").get("pointer_to").get("name")

                    # TODO Slow as hell. Use a map to cache dbs
                    result_db = MongoClient(self.db_url, self.db_port)["tripout"][resource_name]
                    cross_results = result_db.find_one({"_id": ObjectId(resource_id)})

                    if not cross_results:
                        del rendered_el[key]
                    else:
                        cross_results["_id"] = str(cross_results["_id"])
                        rendered_el[key] = cross_results

        return rendered_el

