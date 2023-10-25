from flask import request,jsonify, current_app, Blueprint
from app.models.user import User
from app import db
from app.api.responses import response_with
from app.api import responses as resp

users=Blueprint('users',__name__)

@users.route('')
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
def find(id):
    found=db.get_or_404(User, id)
    return response_with(resp.SUCCESS_200,{'user':found.to_json()})

@users.route('/<int:id>', methods=['PUT'])
def update(id):
    json=request.get_json()
    found=db.get_or_404(User,id)
    found.username=json.get('username',found.username)
    db.session.add(found)
    db.session.commit()
    return response_with(resp.SUCCESS_200,{'user':found.to_json()})

@users.route('/<int:id>', methods=['DELETE'])
def delete(id):
    found=db.get_or_404(User,id)
    db.session.delete(found)
    db.session.commit()
    return response_with(resp.SUCCESS_204)

@users.route('/login', methods=['POST'])
def login():
    
    json = request.get_json()
    
    if json.get('username') is None or json.get('password') is None:
        response_with(resp.UNAUTHORIZED_401, error='username o password mancanti')
    
    user = User.find_by_username(json.get('username'))
    if user is None:
        response_with(resp.UNAUTHORIZED_401, error='Login failed. username o password errati')
    
    if User.check_hash(json.get('password'),user.password):
        response_with(resp.SUCCESS_201,{'access_token':user.id})

    response_with(resp.UNAUTHORIZED_401, error='Login failed. username o password errati')