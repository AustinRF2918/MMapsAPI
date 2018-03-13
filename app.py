"""Starting point of the application. Maps resources to endpoints and runs the application."""

from flask import Flask
from flask_restful import Api

import errors.error_handlers
from resources.decal import Decal, DecalList
from resources.pin import Pin, PinList, PinHashList

# Mapping of blueprint onto Flask application.
app = Flask(__name__)
app.register_blueprint(errors.error_handlers.blueprint)

# Mapping of Flask-RESTful resources to endpoints.
api = Api(app)
api.add_resource(PinList, "/pins/")
api.add_resource(Pin, "/pins/<id>")
api.add_resource(PinHashList, "/pins/hash")

api.add_resource(DecalList, "/decals/")
api.add_resource(Decal, "/decals/<id>")

# Start it!
app.run(debug = True)
