from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

class Pin(Resource):
    def get(self):
        return {"lol": "haha"}

class DecalImage(Resource):
    def get(self):
        return {"url": "blah"}

api.add_resource(Pin, "/pins")
api.add_resource(DecalImage, "/decals")

app.run(debug = True)
