from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from app.api.responses import response_with
from app.api import responses as resp

def admin_required():
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            verify_jwt_in_request()
            claims=get_jwt()
            role=claims['role']
            if role=='ADMIN':
                return fn(*args,**kwargs)
            else:
                return response_with(resp.FORBIDDEN_403_ONLY_ADMIN)
        return decorator
    return wrapper