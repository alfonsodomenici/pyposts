from flask import json,jsonify,request, Blueprint, current_app
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from app import db
from . import api
from .decorators import admin_required
from app.models.user import User
from .responses import response_with
from . import responses as resp
from app.exceptions import NotResourceOwnerError
from app.models.user import user_schema, users_schema

users = Blueprint('users',__name__)

@users.route('/', methods=['GET'])
@admin_required()
def all():
    result=User.query.all()
    return response_with(resp.SUCCESS_200,value={'users':users_schema.dump(result)})

@users.route('/<int:id>')
@jwt_required()
def find(id):
    user=_check_and_find_user(id)
    return response_with(resp.SUCCESS_200,value={'user':user.to_json()})


@users.route('/', methods=['POST'])
def create():
    data = request.get_json()
    current_app.logger.info(data)
    #user = User.from_json(data)
    user = user_schema.load(data)
    user.password=User.generate_hash(user.password)
    db.session.add(user)
    db.session.commit()
    return response_with(resp.SUCCESS_201,value={'user':user.to_json()})

@users.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update(id):
    user = _check_and_find_user(id)
    user.username = request.json.get('username',user.username)
    db.session.add(user)
    db.session.commit()    
    return response_with(resp.SUCCESS_200,value={'user':user.to_json()})


@users.route('/<int:id>', methods=['DELETE'])
@admin_required()
def delete(id):
    user = _check_and_find_user(id)
    db.session.delete(user)
    db.session.commit()
    return response_with(resp.SUCCESS_204)


@users.route('/login', methods=['POST'])
def login():
    data=request.get_json()
    
    if data.get('username') is None or data.get('password') is None:
        return response_with(resp.INVALID_INPUT_422,message='username and password requireds')
    
    user=User.find_by_username(data.get('username'))
    if user is None:
        return response_with(resp.UNAUTHORIZED_401,message='login failed')

    if User.check_hash(data.get('password'),user.password):
        additional_claims={'role':user.role.name}
        token=create_access_token(identity=user.username, additional_claims=additional_claims)
        return response_with(resp.SUCCESS_201,value={'access_token':token})
    
    return response_with(resp.UNAUTHORIZED_401,message='login failed, invalid password')

def _check_and_find_user(id):
    identity = get_jwt_identity()
    logged= User.find_by_username(identity)
    current_app.logger.info(logged.id)
    user = db.get_or_404(User,id)
    current_app.logger.info(user.id)
    if id!=logged.id and not logged.is_admin():
        raise NotResourceOwnerError("id non corrospondente")
    return user
