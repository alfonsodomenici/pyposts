from passlib.hash import pbkdf2_sha256 as sha256
from flask import current_app
from datetime import datetime
from app import db
from app.exceptions import ValidationError,NotResourceOwnerError
from app.models.role import Role


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.now()) 
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)

    def to_json(self):
        return {
            'id':self.id,
            'username':self.username,
            'created_on': self.created_on,
            'role_id': self.role_id
        }

    @staticmethod
    def from_json(json):
        usr=json.get('username')
        pwd=json.get('password')
        role_id=json.get('role_id')
        current_app.logger.info(json)
        if usr is None or usr=='':
            raise ValidationError('User property username is empty')
        if not User.find_by_username(usr) is None:
            raise ValidationError('User property username is not unique')
        if pwd is None or pwd=='':
            raise ValidationError('User property password is empty')
        if role_id is None or role_id=='':
            raise ValidationError('User property role_id is empty')
        if db.session.get(Role, role_id) is None:
            raise ValidationError(f'User property role_id not exsists. id={role_id}')
        hash=User.generate_hash(pwd)
        return User(username=usr,password=hash,role_id=role_id)
    
    @staticmethod
    def generate_hash(pwd):
        return sha256.hash(pwd)
    
    @staticmethod
    def check_hash(pwd,hash):
        return sha256.verify(pwd,hash)

    @staticmethod
    def find_by_username(username):
        return User.query.filter_by(username=username).first()
    
    @classmethod
    def find_by_id_secure(cls,id,claims):
        sub_id=claims['sub_id']
        role=claims['role']
        user = db.get_or_404(cls,id)
        if user.id!=sub_id and role!='ADMIN':
            raise NotResourceOwnerError('not owner')
        return user

    def __repr__(self):
        return '<User {}>'.format(self.username)