"""Schema definition for the decal domain object."""

from flask_restful import fields

decal_schema = {
    "name": "decal",
    "fields": {
        # Base Metadata
        "id": {
            "type": fields.String,
            "required": False,
            "read_only": True,
            "description": "Server generated ID of a decal."
        },

        # Core Domain Data
        "url": {
            "type": fields.String,
            "required": True,
            "read_only": True,
            "description": "Url to given image of a decal."
        }
    },
    "example": {
        "url": "http://www.azure.com/lol", "id": "lolz"
    }
}