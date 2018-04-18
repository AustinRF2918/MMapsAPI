"""Starting point of the application. Maps resources to endpoints and runs the application."""

from flask import Flask
from flask_restful import Api
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS

import errors.error_handlers
from resources.company import CompanyList, Company, CompanyRevisionList
from resources.decal import Decal, DecalList
from resources.pin import Pin, PinList, PinRevisionList

# Mapping of blueprint onto Flask application.
from resources.schema import Schema
from schema.company import company_schema, company_reduced_schema
from schema.decal import decal_schema
from schema.pin import pin_response_schema, pin_request_schema, pin_pointer_schema
from util.schema_tools import register_resource

app = Flask(__name__)
CORS(app)

# Mapping of Flask-RESTful resources to endpoints.
# TODO: Make resource registration nicer.

# Bug with flask restful: we have to overwrite this to use our own.
handle_exception = app.handle_exception
handle_user_exception = app.handle_user_exception
api = Api(app)
app.handle_exception = handle_exception
app.handle_user_exception = handle_user_exception

# Pin Resources
register_resource("/pins/", "pin", "Gets all pin resources", "get", {"200": {"schema": pin_response_schema, "array": True}})
register_resource("/pins/", "pin", "Creates a pin resource", "post", {"201": {"schema": pin_response_schema, "array": False}}, request_type="pin_request")
api.add_resource(PinList, "/pins/")

register_resource("/pins/{id}", "pin", "Gets a pin resource", "get", {"200": {"schema": pin_response_schema, "array": False}}, qparams=["id"])
register_resource("/pins/{id}", "pin", "Deletes a pin resource", "delete", {"200": {"schema": pin_response_schema, "array": False}}, qparams=["id"])
register_resource("/pins/{id}", "pin", "Updates a pin resource", "patch", {"200": {"schema": pin_response_schema, "array": False}}, qparams=["id"], request_type="pin_request")
api.add_resource(Pin, "/pins/<id>")

register_resource("/pins/revisions/", "pin", "Gets all pin resources in a reduced form", "get", {"200": {"schema": pin_pointer_schema, "array": True}})
api.add_resource(PinRevisionList, "/pins/revisions/")

# Pin Resources
register_resource("/companies/", "company", "Gets all company resources", "get", {"200": {"schema": company_schema, "array": True}})
register_resource("/companies/", "company", "Creates a company resource", "post", {"201": {"schema": company_schema, "array": False}}, request_type="company")
api.add_resource(CompanyList, "/companies/")

register_resource("/companies/{id}", "company", "Gets a company resource", "get", {"200": {"schema": company_schema, "array": False}}, qparams=["id"])
register_resource("/companies/{id}", "company", "Deletes a company resource", "delete", {"200": {"schema": company_schema, "array": False}}, qparams=["id"])
register_resource("/companies/{id}", "company", "Updates a company resource", "patch", {"200": {"schema": company_schema, "array": False}}, qparams=["id"])
api.add_resource(Company, "/companies/<id>")

register_resource("/companies/revisions/", "company", "Gets all company resources in a reduced form", "get", {"200": {"schema": company_reduced_schema, "array": True}})
api.add_resource(CompanyRevisionList, "/companies/revisions/")

# Decal Resources
register_resource("/decals/", "decal", "Gets all decal resources", "get", {"200": {"schema": decal_schema, "array": True}})
register_resource("/decals/", "decal", "Creates a decal", "post", {"200": {"schema": decal_schema, "array": False}})
api.add_resource(DecalList, "/decals/")

register_resource("/decals/{id}", "decal", "Gets a decal", "get", {"200": {"schema": decal_schema, "array": False}}, qparams=["id"])
register_resource("/decals/{id}", "decal", "Deletes a decal", "delete", {"200": {"schema": decal_schema, "array": False}}, qparams=["id"])
api.add_resource(Decal, "/decals/<id>")

# Schema Resources
api.add_resource(Schema, "/schema")

# Register Swagger
SWAGGER_URL = '/api/docs'  # URL for exposing Swagger UI (without trailing '/')
API_URL = 'http://localhost:5000/schema'  # Our API url (can of course be a local resource)

# Call factory function to create our blueprint
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
    API_URL,
    config={  # Swagger UI config overrides
        'app_name': "Test application"
    },
    # oauth_config={  # OAuth config. See https://github.com/swagger-api/swagger-ui#oauth2-configuration .
    #    'clientId': "your-client-id",
    #    'clientSecret': "your-client-secret-if-required",
    #    'realm': "your-realms",
    #    'appName': "your-app-name",
    #    'scopeSeparator': " ",
    #    'additionalQueryStringParams': {'test': "hello"}
    # }
)


if __name__ == "__main__":
    # Register blueprint at URL
    # (URL must match the one given to factory function above)
    app.register_blueprint(errors.error_handlers.error_handler)
    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    # Start it!
    app.run(threaded=True, debug=True)
