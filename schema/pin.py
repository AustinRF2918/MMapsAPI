"""Schema definition for the decal pin object as well as its dependencies."""
import copy
from flask_restful import fields

from schema.company import company_schema, company_reduced_schema
from util.schema_tools import fieldize_schema, register_schema

pin_request_schema = register_schema({
    "name": "pin_request",
    "fields": {
        # Base Metadata
        "_id": {
            "type": fields.String,
            "required": False,
            "readOnly": True,
            "description": "Server generated ID of a pin."
        },

        "revision": {
            "type": fields.Integer,
            "required": True,
            "readOnly": True,
            "description": "Server generated revision of a pin."
        },

        # Core Domain Data
        "phone_number": {
            "type": fields.String,
            "required": False,
            "readOnly": False,
            "description": "Phone number a company can be contacted at."
        },
        "description": {
            "type": fields.String,
            "required": True,
            "readOnly": False,
            "description": "Publicly viewable description of a company."
        },
        "address": {
            "type": fields.String,
            "required": True,
            "readOnly": False,
            "description": "Publicly viewable address of a company."
        },
        "image": {
            "type": fields.String,
            "required": False,
            "readOnly": False,
            "description": "Link to the URL of an establishment a company wishes to use."
        },
        "company_data": {
            "type": fields.Nested(fieldize_schema(company_reduced_schema)),
            "required": False,
            "readOnly": False,
            "description": "Company data structure giving more metadata about parent company of an establishment",
            "schema": company_reduced_schema
        },

        # Tagging Metadata
        "tags": {
            "type": fields.List(fields.String),
            "required": False,
            "readOnly": False,
            "description": "List of tags a company wishes to use."
        },

        # Locational Metadata
        "latitude": {
            "type": fields.Float,
            "required": True,
            "readOnly": False,
            "description": "Latitude in float of an establishment."
        },
        "longitude": {
            "type": fields.Float,
            "required": True,
            "readOnly": False,
            "description": "Longitude in float of an establishment."
        },

        # Link Metadata
        "logo_image_link": {
            "type": fields.String,
            "required": False,
            "readOnly": False,
            "description": "Logo of an establishment."
        },
        "social_links": {
            "type": fields.List(fields.String),
            "required": False,
            "readOnly": False,
            "description": "List of social links related to an establishment."
        },
        "website_link": {
            "type": fields.String,
            "required": False,
            "readOnly": False,
            "description": "Link to a website of an establishment."
        }
    },
    "example": {
        "_id": "5aa9e7734700a016fcc12ced",
        "revision": 1,

        "phone_number": "234124",
        "description": "hai",
        "address": "123214 dafdsa",
        "image": "azure.com/fdasfdsa",
        "company_data": {
            "_id": "5aa9e7734700a016fcc12cee",
            "revision": 2,
            "title": "Microsoft",
            "message": "What do you wanna do today?",
            "is_featured": True,
            "is_active": True,
            "photo_stream": ["azure.com/1", "azure.com/2"]
        },

        "tags": ["tech", "soft", "micro"],

        "latitude": 1.3214,
        "longitude": 2.111,

        "logo_image_link": "azure.com/lolzers",
        "social_links": ["facebook.com/microsoft"],
        "website_link": "microsoft.com"
    }
})

# Pin response is just a little different from pin request.
pin_response_schema = copy.deepcopy(pin_request_schema)
pin_response_schema["name"] = "pin_response"
pin_response_schema["fields"]["company_data"]["type"] = fields.Nested(fieldize_schema(company_schema))
pin_response_schema["fields"]["company_data"]["schema"] = company_schema
pin_response_schema = register_schema(pin_response_schema)


pin_pointer_schema = register_schema({
    "name": "pin_reduced",
    "fields": {
        # Base metadata: only contains this
        "_id": {
            "type": fields.String,
            "required": True,
            "readOnly": False,
            "description": "_id pointing to pin resource."
        },
        "revision": {
            "type": fields.Integer,
            "required": True,
            "readOnly": True,
            "description": "revision of pin pointer."
        }
    },
    "example": {
        "_id": "abcdefghi",
        "revision": 1,
    },
    "use_as": "pointer"
})

