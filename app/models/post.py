from passlib.hash import pbkdf2_sha256 as sha256 
from app import db
from app.exceptions import ValidationError
from app.exceptions import NotResourceOwnerError

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    message = db.Column(db.String(512),nullable=False)
    user_id = db.Column(db.Integer,db.ForeignKey('user.id'), nullable=False) 
    
    @classmethod
    def find_by_id_secure(cls,id,claims):
        sub_id=claims['sub_id']
        role=claims['role']
        post=db.get_or_404(cls,id)
        if post.user_id!=sub_id and role!='ADMIN':
            raise NotResourceOwnerError('not owner')
        return post
    
    @classmethod
    def find_by_user_id(cls, user_id):
        return cls.query.filter_by(user_id=user_id).all()

    def __repr__(self):
        return f'<Post {self.message}>'


"""class PostSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Post
        include_fk = True
        load_instance = True
        sqla_session = db.session

    message=ma.auto_field(validate=must_not_be_blank)



postschema = PostSchema()
posts_schema = PostSchema(many=True) """ 