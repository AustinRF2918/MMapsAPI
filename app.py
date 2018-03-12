from flask import Flask
from flask_restful import Api

from pin import PinDao, Pin
from decal_image import DecalImageDao, DecalImage

app = Flask(__name__)
api = Api(app)

api.add_resource(Pin, "/pins")
api.add_resource(DecalImage, "/decals")

app.run(debug = True)
