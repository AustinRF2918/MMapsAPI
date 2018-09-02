"""Schema definition for the decal domain object."""

from flask_restful import fields

from util.schema_tools import register_schema

decal_schema = register_schema({
    "name": "decal",
    "fields": {
        # Base Metadata
        "_id": {
            "type": fields.String,
            "required": False,
            "readOnly": True,
            "description": "Server generated ID of a decal."
        },

        # Core Domain Data
        "url": {
            "type": fields.String,
            "required": True,
            "readOnly": False,
            "description": "Url to given image of a decal."
        }
    },
    "example": {
        "_id": "5aa9e7734700a016fcc12ced",
        "url": "http://www.azure.com/lol"
    }
})
