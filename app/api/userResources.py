from flask import json,jsonify,request, Blueprint
from app import db
from . import api
from ..models import User

@api.route('/users', methods=['GET'])
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

    return jsonify([user.to_json() for user in User.query.all()])

@api.route('/users/<int:id>')
def find_user(id):
    return User.query.get_or_404(id).to_json()

@api.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User.from_json(data)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_json()),201

@api.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    user = User.query.get_or_404(id)
    user.username = request.json.get('username',user.username)
    db.session.add(user)
    db.session.commit()    
    return jsonify(user.to_json())

@api.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return "", 204