from flask import json,jsonify,request, Blueprint, current_app
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required, current_user
from app import db
from . import api
from .decorators import admin_required
from ..models import User

@api.route('/users', methods=['GET'])
@admin_required()
def all_users():
    # ko TypeError: Object of type User is not JSON serializable
    # return User.query.all()  

    # ok content-type application/json
    # return jsonify({'id':1,'username':'rossi'}) 

    # ok content-type application/json
    # return {'id':1,'username':'rossi'} 

    # ok content-type application/json
    # return [{'id':1,'username':'rossi'},{'id':1,'username':'verdi'},{'id':1,'username':'bianchi'}] 
    
    # ok content-type text/html; charset=utf-8
    # return json.dumps({'id':1,'username':'rossi'}) 
    identity = get_jwt_identity()
    current_app.logger.info(f'current identy {identity} {current_user}')
    return jsonify([user.to_json() for user in User.query.all()])

@api.route('/users/<int:id>')
@jwt_required()
def find_user(id):
    if id!=current_user.id and not current_user.is_admin():
        return 'unautorized',401
    return User.query.get_or_404(id).to_json()


@api.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    current_app.logger.info(data)
    user = User.from_json(data)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_json()),201

@api.route('/users/<int:id>', methods=['PUT'])
@jwt_required()
def update_user(id):
    user = User.query.get_or_404(id)
    user.username = request.json.get('username',user.username)
    db.session.add(user)
    db.session.commit()    
    return jsonify(user.to_json())

@api.route('/users/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return "", 204

@api.route('/users/login', methods=['POST'])
def user_login():
    data=request.get_json()
    
    if data.get('username') is None or data.get('password') is None:
        return 'Invalid data.username and password are required',422
    
    user=User.find_by_username(data.get('username'))
    if user is None:
        return 'login failed', 401

    if User.check_hash(data.get('password'),user.password):
        token=create_access_token(identity=user.username)
        return jsonify(access_token=token)
    return 'login failed, bad password',401