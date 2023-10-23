from werkzeug.exceptions import NotFound,HTTPException
from flask_jwt_extended.exceptions import JWTExtendedException
from sqlalchemy.exc import DBAPIError
from flask import jsonify, current_app
from app.exceptions import ValidationError
from . import api
from .responses import response_with
from . import responses as resp

@api.errorhandler(404)
def notFoundError(e):
    current_app.logger.error('Resource not found. {}'.format(e))
    return response_with(resp.SERVER_ERROR_404)

@api.errorhandler(ValidationError)
def validationError(e):
    current_app.logger.error('ValidationError. {}'.format(e.args[0]))
    return response_with(resp.BAD_REQUEST_400, error=e.args[0])

@api.errorhandler(HTTPException)
def httpException(e):
    current_app.logger.error(e)
    return response_with(resp.SERVER_ERROR_500, error=e.__repr__())

@api.errorhandler(DBAPIError)
def dataLayerException(e):
    current_app.logger.error(e)
    return response_with(resp.SERVER_ERROR_500, error=e.__repr__())

@api.errorhandler(JWTExtendedException)
def jwtException(e):
    current_app.logger.error(e)
    return response_with(resp.FORBIDDEN_403, error=e.__repr__())

@api.errorhandler(Exception)
def allException(e):
    current_app.logger.error(e)
    return response_with(resp.SERVER_ERROR_500, error=e.__repr__())