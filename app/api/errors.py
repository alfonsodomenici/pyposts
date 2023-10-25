from flask import current_app, jsonify
from http import HTTPStatus
from flask_jwt_extended.exceptions import JWTExtendedException
from app.api import api
from app.exceptions import ValidationError
from app.api.responses import response_with
from app.api import responses as resp
from app.exceptions import NotResourceOwnerError

@api.errorhandler(ValidationError)
def validationError(e):
    current_app.logger.info(e)
    return response_with(resp.INVALID_INPUT_422,error=e.args[0])

@api.errorhandler(NotResourceOwnerError)
def notResourceOwnerError(e):
    current_app.logger.error('NotResourceOwnerError. {}'.format(e.args[0]))
    return response_with(resp.FORBIDDEN_403, error='You do not own the resource.Admin only')

@api.errorhandler(HTTPStatus.NOT_FOUND)
def resource_not_found(e):
    current_app.logger.info(e)
    return response_with(resp.SERVER_ERROR_404)

@api.errorhandler(JWTExtendedException)
def jwtError(e):
    current_app.logger.info(e)
    return response_with(resp.FORBIDDEN_403, error='Request forbidden')

@api.errorhandler(Exception)
def genericServerError(e):
    current_app.logger.error(e, exc_info=True)
    return response_with(resp.SERVER_ERROR_500, error='Generic error.')