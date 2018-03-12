from flask import Flask, jsonify
from flask_restful import Api

from common import MissingFieldException, ResourceNotFoundException
from pin import Pin, PinList, PinHashList
from decal_image import DecalImageDao, DecalImage

app = Flask(__name__)
api = Api(app)

api.add_resource(PinList, "/pins/")
api.add_resource(Pin, "/pins/<id>")
api.add_resource(PinHashList, "/pins/hash")
api.add_resource(DecalImage, "/decals")

# Global error handler for the application. If this gets more complex, move this
# to its own file.
@app.errorhandler(MissingFieldException)
def handle_invalid_usage(error):
    return jsonify({
        "type": type(error).__name__,
        "message": error.message,
        "missing_field": error.field_name
    }), 500

@app.errorhandler(ResourceNotFoundException)
def handle_invalid_usage(error):
    return jsonify({
        "type": type(error).__name__,
        "message": error.message,
        "resource": error.resource,
        "uuid": error.uuid
    }), 500

@app.errorhandler(Exception)
def handle_invalid_usage(error):
    return jsonify({
        "type": type(error).__name__,
        "message": str(error)
    }), 500

app.run(debug = True)
