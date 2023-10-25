from flask import jsonify,request, current_app, Blueprint
from app.models.role import Role
from app import db
from app.api.responses import response_with
from app.api import responses as resp

roles=Blueprint('roles',__name__)

@roles.route('')
def all():
    result=[role.to_json() for role in Role.query.all()]
    return response_with(resp.SUCCESS_200,{'roles':result})

@roles.route('',methods=['POST'])
def create():
    json = request.get_json()
    current_app.logger.info(json)
    role = Role.from_json(json)
    db.session.add(role)
    db.session.commit()
    return response_with(resp.SUCCESS_201,{'role':role.to_json()})

@roles.route('/<int:id>')
def find(id):
    found = db.get_or_404(Role, id)
    return response_with(resp.SUCCESS_200,{'role':found.to_json()})

@roles.route('/<int:id>', methods=['PUT'])
def update(id):
    json = request.get_json()
    current_app.logger.info(json)
    found = db.get_or_404(Role, id)
    found.name = json.get('name',found.name)
    db.session.add(found)
    db.session.commit()
    return response_with(resp.SUCCESS_200,{'role':found.to_json()})

@roles.route('/<int:id>', methods=['DELETE'])
def delete(id):
    found=db.get_or_404(Role,id)
    db.session.delete(found)
    db.session.commit()
    return response_with(resp.SUCCESS_204)

