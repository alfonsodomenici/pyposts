from flask import jsonify,request, current_app, Blueprint
from app.models.role import Role
from app import db

roles=Blueprint('roles',__name__)

@roles.route('')
def all():
    return jsonify([role.to_json() for role in Role.query.all()])

@roles.route('',methods=['POST'])
def create():
    json = request.get_json()
    current_app.logger.info(json)
    role = Role.from_json(json)
    db.session.add(role)
    db.session.commit()
    return jsonify(role.to_json()),201

@roles.route('/<int:id>')
def find(id):
    found = db.get_or_404(Role, id)
    return jsonify(found.to_json())

@roles.route('/<int:id>', methods=['PUT'])
def update(id):
    json = request.get_json()
    current_app.logger.info(json)
    found = db.get_or_404(Role, id)
    found.name = json.get('name',found.name)
    db.session.add(found)
    db.session.commit()
    return jsonify(found.to_json())

@roles.route('/<int:id>', methods=['DELETE'])
def delete(id):
    found=db.get_or_404(Role,id)
    db.session.delete(found)
    db.session.commit()
    return "",204

