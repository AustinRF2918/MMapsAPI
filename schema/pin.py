"""Schema definition for the decal pin object as well as its dependencies."""
from flask_restful import fields

from util.schema_tools import fieldize_schema

company_schema = {
    "name": "company",
    "fields": {
        # Core Domain Data
        "title": {
            "type": fields.String,
            "required": True,
            "read_only": False,
            "description": "The name of a company that a company wishes to set as publicly viewable."
        },
        "message": {
            "type": fields.String,
            "required": True,
            "read_only": False,
            "description": "The message a company wishes to set as publicly viewable."
        },
        "is_featured": {
            "type": fields.Boolean,
            "required": True,
            "read_only": False,
            "description": "If a company has been featured by the client or not."
        },
        "photo_stream": {
            "type": fields.List(fields.String),
            "required": False,
            "read_only": False,
            "description": "Optional list of photo URLs a company wishes to display."
        }
    },
    "example": {
        "title": "Microsoft",
        "message": "What do you wanna do today?",
        "is_featured": True,
        "photo_stream": ["azure.com/1", "azure.com/2"]
    }
}

pin_schema = {
    "name": "pin",
    "fields": {
        # Base Metadata
        "id": {
            "type": fields.String,
            "required": False,
            "read_only": True,
            "description": "Server generated ID of a pin."
        },

        "hash": {
            "type": fields.String,
            "required": False,
            "read_only": True,
            "description": "Server generated hash of a pin."
        },

        # Core Domain Data
        "phone_number": {
            "type": fields.String,
            "required": False,
            "read_only": False,
            "description": "Phone number a company can be contacted at."
        },
        "description": {
            "type": fields.String,
            "required": True,
            "read_only": False,
            "description": "Publicly viewable description of a company."
        },
        "address": {
            "type": fields.String,
            "required": True,
            "read_only": False,
            "description": "Publicly viewable address of a company."
        },
        "image": {
            "type": fields.String,
            "required": False,
            "read_only": False,
            "description": "Link to the URL of an establishment a company wishes to use."
        },
        "company_data": {
            "type": fields.Nested(fieldize_schema(company_schema)),
            "required": False,
            "read_only": False,
            "description": "Company data structure giving more metadata about parent company of an establishment",
            "schema": company_schema
        },

        # Tagging Metadata
        "tags": {
            "type": fields.List(fields.String),
            "required": False,
            "read_only": False,
            "description": "List of tags a company wishes to use."
        },

        # Locational Metadata
        "latitude": {
            "type": fields.Float,
            "required": True,
            "read_only": False,
            "description": "Latitude in float of an establishment."
        },
        "longitude": {
            "type": fields.Float,
            "required": True,
            "read_only": False,
            "description": "Longitude in float of an establishment."
        },

        # Link Metadata
        "logo_image_link": {
            "type": fields.String,
            "required": False,
            "read_only": False,
            "description": "Logo of an establishment."
        },
        "social_links": {
            "type": fields.List(fields.String),
            "required": False,
            "read_only": False,
            "description": "List of social links related to an establishment."
        },
        "website_link": {
            "type": fields.String,
            "required": False,
            "read_only": False,
            "description": "Link to a website of an establishment."
        }
    },
    "example": {
        "id": "abcdefghi",
        "hash": "lolz",

        "phone_number": "234124",
        "description": "hai",
        "address": "123214 dafdsa",
        "image": "azure.com/fdasfdsa",
        "company_data": {
            "title": "Microsoft",
            "message": "What do you wanna do today?",
            "is_featured": True,
            "photo_stream": ["azure.com/1", "azure.com/2"]
        },

        "tags": ["tech", "soft", "micro"],

        "latitude": 1.3214,
        "longitude": 2.111,

        "logo_image_link": "azure.com/lolzers",
        "social_links": ["facebook.com/microsoft"],
        "website_link": "microsoft.com"
    }
}

pin_reduced_schema = {
    "name": "pin_reduced",
    "fields": {
        # Base metadata: only contains this
        "id": pin_schema["fields"]["id"],
        "hash": pin_schema["fields"]["hash"]
    },
    "example": {
        "id": "abcdefghi",
        "hash": "lolz",
    }
}