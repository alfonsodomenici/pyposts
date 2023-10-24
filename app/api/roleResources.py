from flask import json,jsonify,request, Blueprint
from flask_jwt_extended import jwt_required
from app import db
from . import api
from ..models import Role
from .decorators import admin_required

roles = Blueprint('roles',__name__)

@roles.route('/', methods=['GET'])
@jwt_required()
def all():
    return jsonify([role.to_json() for role in Role.query.all()])

@roles.route('/<int:id>')
@jwt_required
def find(id):
    return db.get_or_404(Role,id).to_json()

@roles.route('/', methods=['POST'])
@admin_required()
def create():
    role = Role.from_json(request.json)
    db.session.add(role)
    db.session.commit()
    return jsonify(role.to_json()),201

@roles.route('/<int:id>', methods=['PUT'])
@admin_required()
def update(id):
    role = db.get_or_404(Role,id)
    role.username = request.json.get('name',role.name)
    db.session.add(role)
    db.session.commit()    
    return jsonify(role.to_json())

@roles.route('/<int:id>', methods=['DELETE'])
@admin_required()
def delete(id):
    role = db.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    return "", 204