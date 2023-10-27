from app import db
from app.exceptions import ValidationError, NotResourceOwnerError
from app.models.user import User

class Post(db.Model):
    __tablename__ = 'post'
    id=db.Column(db.Integer,primary_key=True)
    message=db.Column(db.String(512), nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    @staticmethod
    def find_by_user_id(user_id):
        return Post.query.filter_by(user_id=user_id).all()

    @classmethod
    def find_by_id_secure(cls,id,claims):
        sub_id=claims['sub_id']
        role=claims['role']
        post = db.get_or_404(cls,id)
        if post.user_id!=sub_id and role!='ADMIN':
            raise NotResourceOwnerError('not owner')
        return post 
