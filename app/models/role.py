from marshmallow import fields
from datetime import datetime
from passlib.hash import pbkdf2_sha256 as sha256 
from app import db,ma
from app.exceptions import ValidationError

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    users = db.relationship('User', backref='role', cascade="all, delete-orphan")
    
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
    

"""class RoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Role
        load_instance = True
        sqla_session = db.session

    name=ma.auto_field(validate=must_not_be_blank)

role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)   """

