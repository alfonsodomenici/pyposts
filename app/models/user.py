from marshmallow import fields
from datetime import datetime
from passlib.hash import pbkdf2_sha256 as sha256 
from flask import current_app
from app import db
from app.exceptions import ValidationError
from app.datetimes import format_dt
from app.models.role import Role
from app import ma
from app.models.schemas import must_not_be_blank

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.now()) 
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    role = db.relationship("Role", backref="users")

    @staticmethod
    def generate_hash(pwd):
        return sha256.hash(pwd) 
    
    @staticmethod
    def check_hash(pwd,hash):
        return sha256.verify(pwd,hash)
    
    def to_json(self):
        return {
            'id':self.id,
            'username':self.username,
            'created_on':format_dt(self.created_on),
            'role_id': self.role_id
        }
    
    def from_json(user_json):
        username=user_json.get('username')
        password=user_json.get('password')
        role_id=user_json.get('role_id')
        if username is None or username == '':
            raise ValidationError('username vuoto')
        if password is None or password == '':
            raise ValidationError('password vuota')
        if role_id is None or db.session.get(Role,role_id) is None:
            raise ValidationError('role vuota o inesistente role_id:{}'.format(role_id))
        hash=sha256.hash(user_json.get('password')) 
        return User(username=username,password=hash,role_id=role_id)
    
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    def is_admin(self):
        return self.role.name=='ADMIN'

    def __repr__(self):
        return '<User {}>'.format(self.username)
    

"""class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
        include_fk = True
        load_instance = True
        sqla_session = db.session

    username=ma.auto_field(validate=must_not_be_blank)
    password=ma.auto_field(load_only=True, validate=must_not_be_blank)
    created_on=ma.auto_field(dump_only=True)

user_schema = UserSchema()
users_schema = UserSchema(many=True)   """

class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        sqla_session = db.session

    id=fields.Int(dump_only=True)
    username=fields.String(required=True, validate=must_not_be_blank)
    password=fields.String(load_only=True, validate=must_not_be_blank)
    created_on=fields.String(dump_only=True)
    role_id=fields.Int(required=True)
    
user_schema = UserSchema()
users_schema = UserSchema(many=True)   