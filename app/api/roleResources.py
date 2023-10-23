from flask import json,jsonify,request, Blueprint
from flask_jwt_extended import jwt_required
from app import db
from . import api
from ..models import Role
from .decorators import admin_required

@api.route('/roles', methods=['GET'])
@jwt_required()
def all_roles():
    return jsonify([role.to_json() for role in Role.query.all()])

@api.route('/roles/<int:id>')
@jwt_required
def find_role(id):
    return Role.query.get_or_404(id).to_json()

@api.route('/roles', methods=['POST'])
@admin_required()
def create_role():
    role = Role.from_json(request.json)
    db.session.add(role)
    db.session.commit()
    return jsonify(role.to_json()),201

@api.route('/roles/<int:id>', methods=['PUT'])
@admin_required()
def update_role(id):
    role = Role.query.get_or_404(id)
    role.username = request.json.get('name',role.name)
    db.session.add(role)
    db.session.commit()    
    return jsonify(role.to_json())

@api.route('/roles/<int:id>', methods=['DELETE'])
@admin_required()
def delete_role(id):
    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    return "", 204