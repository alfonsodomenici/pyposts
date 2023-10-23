from datetime import datetime
from passlib.hash import pbkdf2_sha256 as sha256 
from flask import current_app
from app import db
from app.exceptions import ValidationError
from datetime_utils import format_dt

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)

    users = db.relationship('User', backref='role')

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
    
    def __repr__(self):
        return '<Role {}>'.format(self.name)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.now()) 
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

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
        if role_id is None or Role.query.get(role_id) is None:
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


