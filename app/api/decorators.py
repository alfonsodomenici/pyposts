from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from app.models import User

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
                return jsonify(msg="Admins only!"), 403
        return decorator
    return wrapper