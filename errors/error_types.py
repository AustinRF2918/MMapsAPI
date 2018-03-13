"""
Custom error types located in this file. If a new type is created, it
must be registered as an @app.errorhandler in errors/error_handlers.py!
"""

class MissingFieldException(Exception):
    def __init__(self, field_name):
        self.field_name = field_name
        self.message = "Field {} was omitted, but is required!".format(field_name)


class ResourceNotFoundException(Exception):
    def __init__(self, resource, resource_id):
        self.resource = resource
        self.resource_id = resource_id
        self.message = "Could not find {} with uuid {}.".format(resource, resource_id)


