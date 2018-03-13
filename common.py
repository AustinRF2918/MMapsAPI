from flask_restful import fields


class MissingFieldException(Exception):
    def __init__(self, field_name):
        self.field_name = field_name
        self.message = "Field {} was omitted, but is required!".format(field_name)

class ResourceNotFoundException(Exception):
    def __init__(self, resource, uuid):
        self.resource = resource
        self.uuid = uuid
        self.message = "Could not find {} with uuid {}.".format(resource, uuid)

