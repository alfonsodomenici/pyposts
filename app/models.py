from passlib.hash import pbkdf2_sha256 as sha256
from app import db
from app.exceptions import ValidationError

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
        if role_id is None:
            raise ValidationError('role vuota')
        Role.query.get_or_404(role_id)
        password=User.generate_hash(password)
        return User(username=username,password=password,role_id=role_id)

    def __repr__(self):
        return '<User {}>'.format(self.username)


