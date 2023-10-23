from werkzeug.exceptions import NotFound,HTTPException
from flask import jsonify, current_app
from app.exceptions import ValidationError
from . import api


def bad_request(message):
    response = jsonify({'error': 'bad request', 'message': message})
    response.status_code = 400
    return response

@api.errorhandler(404)
def notFoundError(e):
    current_app.logger.error('Resource not found. {}'.format(e))
    return jsonify('Resource non found',404)

@api.errorhandler(ValidationError)
def validationError(e):
    current_app.logger.error('ValidationError. {}'.format(e.args[0]))
    return bad_request(e.args[0])

@api.errorhandler(HTTPException)
def httpException(e):
    current_app.logger.error(e)
    return jsonify(e.description, e.code)