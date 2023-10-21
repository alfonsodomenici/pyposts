from flask import json,jsonify,request, Blueprint
from app import db
from . import api
from ..models import Role


@api.route('/roles', methods=['GET'])
def all_roles():
    return jsonify([role.to_json() for role in Role.query.all()])

@api.route('/roles/<int:id>')
def find_role(id):
    return Role.query.get_or_404(id).to_json()

@api.route('/roles', methods=['POST'])
def create_role():
    role = Role.from_json(request.json)
    db.session.add(role)
    db.session.commit()
    return jsonify(role.to_json()),201

@api.route('/roles/<int:id>', methods=['PUT'])
def update_role(id):
    role = Role.query.get_or_404(id)
    role.username = request.json.get('name',role.name)
    db.session.add(role)
    db.session.commit()    
    return jsonify(role.to_json())

@api.route('/roles/<int:id>', methods=['DELETE'])
def delete_role(id):
    role = Role.query.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    return "", 204