from flask import current_app, jsonify
from http import HTTPStatus
from app.api import api
from app.exceptions import ValidationError

@api.errorhandler(ValidationError)
def validationError(e):
    current_app.logger.info(e)
    return jsonify({'error':e.args[0]}), HTTPStatus.BAD_REQUEST

@api.errorhandler(HTTPStatus.NOT_FOUND)
def resource_not_found(e):
    current_app.logger.info(e)
    return jsonify({'error':'resource not found'}),HTTPStatus.NOT_FOUND
