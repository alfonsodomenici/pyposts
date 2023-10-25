from app import db
from app.exceptions import ValidationError

class Role(db.Model):
    __tablename__ = 'role'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True)
    users=db.relationship('User', backref='role')

    def to_json(self):
        return {
            'id':self.id,
            'name': self.name
        }
    
    @staticmethod
    def from_json(json):
        name=json.get('name')
        if name is None or name=='':
            raise ValidationError('Role property name is empty')
        return Role(name=name)
    
    def __repr__(self):
        return '<Role {}>'.format(self.name)