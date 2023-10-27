from app import db

class Post(db.Model):
    __tablename__ = 'post'
    id=db.Column(db.Integer,primary_key=True)
    message=db.Column(db.String(512), nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)