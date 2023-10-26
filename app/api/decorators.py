import json
from flask import current_app
from functools import wraps
from flask_jwt_extended import verify_jwt_in_request, get_jwt
from app.api.responses import response_with
from app.api import responses as resp
from app.exceptions import NotResourceOwnerError

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

def resource_owner_required(payload_name: str ='user',payload_field: int ='id'):
    def wrapper(fn):
        @wraps(fn)
        def decorator(*args, **kwargs):
            try:
                verify_jwt_in_request()
                claims=get_jwt()
                role=claims['role']
                sub_id=claims['sub_id']
                result = fn(*args,**kwargs)
                payload=json.loads(result.response[0])
                current_app.logger.info(result.response)
                if payload[payload_name][payload_field] != sub_id and role != 'ADMIN':
                    raise NotResourceOwnerError('not owner..')
                return result
            except Exception as e:
                current_app.logger.error(e,exc_info=True)
                raise NotResourceOwnerError('error i decorator')
        return decorator
    return wrapper