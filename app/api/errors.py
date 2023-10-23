from werkzeug.exceptions import NotFound,HTTPException
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
    return response_with(resp.BAD_REQUEST_400, message=e.args[0])

@api.errorhandler(HTTPException)
def httpException(e):
    current_app.logger.error(e)
    return response_with(resp.SERVER_ERROR_500, message=e.description)

