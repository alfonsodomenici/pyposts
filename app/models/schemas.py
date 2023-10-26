from marshmallow import ValidationError 
from marshmallow import fields
from app import ma,db
from app.models.role import Role
from app.models.user import User
from app.models.post import Post

# Custom validator
def must_not_be_blank(data):
    if not data or str(data).isspace():
        raise ValidationError("Data not provided.")


class PostSchema(ma.SQLAlchemySchema):
    class Meta:
        model=Post
        load_instance = True
        sqla_session=db.session
    
    id=fields.Int(dump_only=True)
    message=fields.String(required=True)
    user_id=fields.Int(dump_only=True)
    
class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = User
        load_instance = True
        sqla_session = db.session

    id=fields.Int(dump_only=True)
    username=fields.String(required=True, validate=must_not_be_blank)
    password=fields.String(load_only=True, validate=must_not_be_blank)
    created_on=fields.String(dump_only=True)
    role_id=fields.Int(required=True)
    posts=fields.Nested(PostSchema, many=True, only=['message','id'])
    
class RoleSchema(ma.SQLAlchemySchema):
    class Meta:
        model = Role
        load_instance = True
        sqla_session = db.session

    id=fields.Int(dump_only=True)
    name=fields.String(required=True)
    users=fields.Nested(UserSchema, many=True, only=['username','id'])


role_schema = RoleSchema()
roles_schema = RoleSchema(many=True)
user_schema = UserSchema()
users_schema = UserSchema(many=True)  
post_schema = PostSchema()
posts_schema = PostSchema(many=True)



 





