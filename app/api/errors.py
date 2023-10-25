from flask import current_app, jsonify
from http import HTTPStatus
from app.api import api
from app.exceptions import ValidationError
from app.api.responses import response_with
from app.api import responses as resp

@api.errorhandler(ValidationError)
def validationError(e):
    current_app.logger.info(e)
    return response_with(resp.INVALID_INPUT_422,error=e.args[0])

@api.errorhandler(HTTPStatus.NOT_FOUND)
def resource_not_found(e):
    current_app.logger.info(e)
    return response_with(resp.SERVER_ERROR_404)

@api.errorhandler(Exception)
def genericServerError(e):
    current_app.logger.info(e)
    return response_with(resp.SERVER_ERROR_500, error='Generic error.')