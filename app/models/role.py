from datetime import datetime
from passlib.hash import pbkdf2_sha256 as sha256 
from flask import current_app
from app import db
from app.exceptions import ValidationError
from app.datetimes import format_dt
from app import ma
from app.models.schemas import must_not_be_blank

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    #users = db.relationship('User', backref='role')

    def to_json(self):
        return {
            'id':self.id,
            'name':self.name
        }
    
    def from_json(json):
        current_app.logger.info(json)
        name=json.get('name')
        if name is None or name == '':
            raise ValidationError('role name vuoto')
        return Role(name=name)
    
    @staticmethod
    def insert_roles():
        default_roles=[Role(name='ADMIN'),Role(name='USER')]
        roles = Role.query.all()
        [db.session.add(role) for role in default_roles if role not in roles ]
        db.session.commit
    
    def __eq__(self, other):
        return self.name == other.name

    def __repr__(self):
        return '<Role {}>'.format(self.name)
    

class RoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Role
        load_instance = True
        sqla_session = db.session

    name=ma.auto_field(validate=must_not_be_blank)

role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)   