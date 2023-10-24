from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from app.models.user import User
from .responses import response_with
from . import responses as resp

def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims=get_jwt()
            role=claims['role']
            if role == 'ADMIN':
                return fn(*args,**kwargs)
            else:
                return response_with(resp.FORBIDDEN_403,error='Admin only')
        return decorator
    return wrapper