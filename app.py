from flask import Flask
from flask_restful import Api

from pin import Pin, PinList
from decal_image import DecalImageDao, DecalImage

app = Flask(__name__)
api = Api(app)

api.add_resource(PinList, "/pins/")
api.add_resource(DecalImage, "/decals")

app.run(debug = True)
