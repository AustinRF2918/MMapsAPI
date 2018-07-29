"""Defines Pin resource."""
from flask import request
from flask_restful import Resource

from schema.company import company_schema, company_reduced_schema
from util.schema_tools import marshal_with_schema
from util.dao import MongoDao

company_dao = MongoDao(company_schema, "localhost", 27017)


class CompanyList(Resource):
    def get(self):
        return company_dao.get_all()

    def post(self):
        company = request.get_json(force=True)
        return company_dao.add_item(company)


class CompanyRevisionList(Resource):
    def get(self):
        return company_dao.get_all()


class Company(Resource):
    """Domain object for Michigan Maps company. More docs to go here."""

    def get(self, id):
        return company_dao.get_item(id)

    def delete(self, id):
        return company_dao.delete_item(id)

    def patch(self, id):
        new_fields = request.get_json(force=True)
        return company_dao.update_item(id, new_fields)
