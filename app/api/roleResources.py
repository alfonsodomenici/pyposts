from flask import json,jsonify,request, Blueprint
from flask_jwt_extended import jwt_required
from app import db
from . import api
from app.models.role import Role, role_schema, roles_schema
from .decorators import admin_required
from app.api.responses import response_with
from app.api import responses as resp

roles = Blueprint('roles',__name__)

@roles.route('/', methods=['GET'])
@admin_required()
def all():
    result=Role.query.all()
    return response_with(resp.SUCCESS_200,value={'roles':roles_schema.dump(result)})

@roles.route('/<int:id>')
@admin_required()
def find(id):
    result=db.get_or_404(Role,id)
    return response_with(resp.SUCCESS_200,value={'role':role_schema.dump(result)})

@roles.route('/', methods=['POST'])
@admin_required()
def create():
    role = role_schema.load(request.json)
    db.session.add(role)
    db.session.commit()
    return response_with(resp.SUCCESS_201,value={'role':role_schema.dump(role)})

@roles.route('/<int:id>', methods=['PUT'])
@admin_required()
def update(id):
    role = db.get_or_404(Role,id)
    role.name = request.json.get('name',role.name)
    db.session.add(role)
    db.session.commit()    
    return response_with(resp.SUCCESS_200,value={'role':role_schema.dump(role)})

@roles.route('/<int:id>', methods=['DELETE'])
@admin_required()
def delete(id):
    role = db.get_or_404(id)
    db.session.delete(role)
    db.session.commit()
    return response_with(resp.SUCCESS_204)