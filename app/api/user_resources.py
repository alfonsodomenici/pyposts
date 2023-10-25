from flask import request,jsonify, current_app, Blueprint
from app.models.user import User
from app import db
from app.api.responses import response_with
from app.api import responses as resp
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.api.decorators import admin_required
from app.exceptions import NotResourceOwnerError

users=Blueprint('users',__name__)

@users.route('')
@admin_required()
def all():
    result = [user.to_json() for user in User.query.all()]
    return response_with(resp.SUCCESS_200, {'users':result})

@users.route('', methods=['POST'])
def create():
    json = request.get_json()
    user = User.from_json(json)
    db.session.add(user)
    db.session.commit()
    return response_with(resp.SUCCESS_201,{'user':user.to_json()})

@users.route('/<int:id>')
@jwt_required()
def find(id):
    logged_user=_check_and_find_user(id)
    found=db.get_or_404(User,id)
    return response_with(resp.SUCCESS_200,{'user':found.to_json()})

@users.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update(id):
    json=request.get_json()
    found=db.get_or_404(User,id)
    found.username=json.get('username',found.username)
    db.session.add(found)
    db.session.commit()
    return response_with(resp.SUCCESS_200,{'user':found.to_json()})

@users.route('/<int:id>', methods=['DELETE'])
@admin_required()
def delete(id):
    found=db.get_or_404(User,id)
    db.session.delete(found)
    db.session.commit()
    return response_with(resp.SUCCESS_204)

@users.route('/login', methods=['POST'])
def login():
    
    json = request.get_json()
    
    if json.get('username') is None or json.get('password') is None:
        return response_with(resp.UNAUTHORIZED_401, error='username o password mancanti')
    
    user = User.find_by_username(json.get('username'))
    if user is None:
        return response_with(resp.UNAUTHORIZED_401, error='Login failed. username o password errati')
    
    if User.check_hash(json.get('password'),user.password):
        additional_claims={'role':user.role.name}
        token=create_access_token(identity=user.username, additional_claims=additional_claims)
        return response_with(resp.SUCCESS_201,value={'access_token':token})

    return response_with(resp.UNAUTHORIZED_401, error='Login failed. username o password errati')

def _check_and_find_user(id):
    logged_user=get_jwt_identity()
    db_logged=User.find_by_username(logged_user)
    if db_logged.role.name=='USER' and id!=db_logged.id:
        raise NotResourceOwnerError('id non corrispondente')
    return db_logged