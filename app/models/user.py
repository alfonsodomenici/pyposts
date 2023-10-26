from datetime import datetime
from passlib.hash import pbkdf2_sha256 as sha256 
from app import db
from app.exceptions import ValidationError
from app.exceptions import NotResourceOwnerError

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(50), nullable=False)
    created_on = db.Column(db.DateTime, default=datetime.now()) 
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'), nullable=False)
    posts = db.relationship('Post', backref='user', cascade="all, delete-orphan")

    @staticmethod
    def generate_hash(pwd):
        return sha256.hash(pwd) 
    
    @staticmethod
    def check_hash(pwd,hash):
        return sha256.verify(pwd,hash)
    
    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
    
    @classmethod
    def find_by_id_secure(cls,id,claims):
        sub_id=claims['sub_id']
        role=claims['role']
        user=db.get_or_404(cls,id)
        if user.id!=sub_id and role!='ADMIN':
            raise NotResourceOwnerError('not owner')
        return user
    
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
