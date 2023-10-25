from flask import request,jsonify, current_app, Blueprint
from app.models.user import User
from app import db

users=Blueprint('users',__name__)

@users.route('')
def all():
    return jsonify([user.to_json() for user in User.query.all()])

@users.route('', methods=['POST'])
def create():
    json = request.get_json()
    user = User.from_json(json)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_json())

@users.route('/<int:id>')
def find(id):
    found=db.get_or_404(User, id)
    return jsonify(found.to_json())

@users.route('/<int:id>', methods=['PUT'])
def update(id):
    json=request.get_json()
    found=db.get_or_404(User,id)
    found.username=json.get('username',found.username)
    db.session.add(found)
    db.session.commit()
    return jsonify(found.to_json())

@users.route('/<int:id>', methods=['DELETE'])
def delete(id):
    found=db.get_or_404(User,id)
    db.session.delete(found)
    db.session.commit()
    return '',204