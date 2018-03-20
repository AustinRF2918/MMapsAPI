"""
Custom error handlers located in this file.
"""
import traceback

from flask import jsonify, Blueprint

from errors.error_types import MissingFieldException, ResourceNotFoundException

error_handler = Blueprint("errors.error_handlers", __name__)


@error_handler.app_errorhandler(MissingFieldException)
def handle_missing_field(error):
    return jsonify({
        "type": type(error).__name__,
        "message": error.message,
        "missing_field": error.field_name
    }), 500


@error_handler.app_errorhandler(ResourceNotFoundException)
def handle_resource_not_found(error):
    return jsonify({
        "type": type(error).__name__,
        "message": error.message,
        "resource": error.resource,
        "resource_id": error.resource_id
    }), 403


@error_handler.app_errorhandler(Exception)
def handle_generic_exception(error):
    traceback.print_tb(error.__traceback__)

    return jsonify({
        "type": type(error).__name__,
        "message": str(error)
    }), 500