"""Schema definition for the company domain object."""

from flask_restful import fields

from util.schema_tools import register_schema

company_schema = register_schema({
    "name": "company",
    "fields": {
        # Base Metadata
        "_id": {
            "type": fields.String,
            "required": True,
            "readOnly": True,
            "description": "Database generated uniqueId of a company."
        },

        "revision": {
            "type": fields.Integer,
            "required": False,
            "readOnly": True,
            "description": "Server generated revision of a pin."
        },

        # Core Domain Data
        "title": {
            "type": fields.String,
            "required": True,
            "readOnly": False,
            "description": "The name of a company that a company wishes to set as publicly viewable."
        },
        "message": {
            "type": fields.String,
            "required": True,
            "readOnly": False,
            "description": "The message a company wishes to set as publicly viewable."
        },
        "is_featured": {
            "type": fields.Boolean,
            "required": True,
            "readOnly": False,
            "description": "If a company has been featured by the client or not."
        },
        "is_active": {
            "type": fields.Boolean,
            "required": True,
            "readOnly": False,
            "description": "If a company has been registered as active by the client"
        },
        "photo_stream": {
            "type": fields.List(fields.String),
            "required": False,
            "readOnly": False,
            "description": "Optional list of photo URLs a company wishes to display."
        }
    },
    "example": {
        "_id": "5aa9e7734700a016fcc12ced",
        "revision": 1,
        "title": "Microsoft",
        "message": "What do you wanna do today?",
        "is_featured": True,
        "is_active": True,
        "photo_stream": ["azure.com/1", "azure.com/2"]
    }
})

company_reduced_schema = register_schema({
    "name": "company_reduced",
    "fields": {
        # Base metadata: only contains this
        "_id": {
            "type": fields.String,
            "required": True,
            "readOnly": True,
            "description": "_id pointing to company resource."
        },
        "revision": {
            "type": fields.Integer,
            "required": False,
            "readOnly": True,
            "description": "revision of company pointer."
        }
    },
    "example": {
        "_id": "abcdefghi",
        "revision": 1,
    },
    "pointer_to": company_schema
})
