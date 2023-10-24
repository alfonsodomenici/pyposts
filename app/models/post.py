from datetime import datetime
from passlib.hash import pbkdf2_sha256 as sha256 
from flask import current_app
from app import db
from app.exceptions import ValidationError
from app.datetimes import format_dt

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    message = db.Column(db.String(512),nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False)

    @staticmethod
    def from_json(json):
        if json.get('message') is None or json.get('message') == '':
            raise ValidationError('message vuoto')
        return Post(message=json.get('message'))  

    def to_json(self):
        return {
            'id':self.id,
            'message':self.message,
            'user_id':self.user_id
        }  
    
    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    def __repr__(self):
        return f'<Post {self.message}>'
    