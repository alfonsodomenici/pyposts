from flask import jsonify,request, current_app, Blueprint
from app.models.role import Role
from app import db
from app.api.responses import response_with
from app.api import responses as resp
from flask_jwt_extended import jwt_required
from app.api.decorators import admin_required
from app.models.schemas import role_schema,roles_schema

roles=Blueprint('roles',__name__)

@roles.route('')
@admin_required()
def all():
    result=Role.query.all()
    return response_with(resp.SUCCESS_200,{'roles':roles_schema.dump(result)})

@roles.route('',methods=['POST'])
@admin_required()
def create():
    json = request.get_json()
    current_app.logger.info(json)
    role = role_schema.load(json)
    db.session.add(role)
    db.session.commit()
    return response_with(resp.SUCCESS_201,{'role':role_schema.dump(role)})

@roles.route('/<int:id>')
@admin_required()
def find(id):
    found = db.get_or_404(Role, id)
    return response_with(resp.SUCCESS_200,{'role':role_schema.dump(found)})

@roles.route('/<int:id>', methods=['PUT'])
@admin_required()
def update(id):
    json = request.get_json()
    current_app.logger.info(json)
    found = db.get_or_404(Role, id)
    found.name = json.get('name',found.name)
    db.session.add(found)
    db.session.commit()
    return response_with(resp.SUCCESS_200,{'role':role_schema.dump(found)})

@roles.route('/<int:id>', methods=['DELETE'])
@admin_required()
def delete(id):
    found=db.get_or_404(Role,id)
    db.session.delete(found)
    db.session.commit()
    return response_with(resp.SUCCESS_204)

