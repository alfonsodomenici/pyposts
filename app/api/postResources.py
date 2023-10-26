from flask import request, current_app, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from .decorators import admin_required
from .responses import response_with
from . import responses as resp
from . import api
from app.models.user import User
from app.models.post import Post
from app.models.schemas import posts_schema, post_schema
from app import db
from app.exceptions import NotResourceOwnerError

posts = Blueprint('posts',__name__)

@posts.route('/')
@jwt_required()
def all():
    jwt=get_jwt()
    result = Post.query.all() if jwt.get('role')=='ADMIN' else Post.find_by_user_id(jwt.get('sub_id'))
    return response_with(resp.SUCCESS_200,value={'posts':posts_schema.dump(result)})

@posts.route('/<int:id>')
@jwt_required()
def find(id):
    post= Post.find_by_id_secure(id,get_jwt())
    return response_with(resp.SUCCESS_200,value={'post':post_schema.dump(post)})


@posts.route('/', methods=['POST'])
@jwt_required()
def create():
    sub_id=get_jwt().get('sub_id')
    post = post_schema.load(request.get_json())
    post.user_id=sub_id
    db.session.add(post)
    db.session.commit()
    return response_with(resp.SUCCESS_201,value={'post':post_schema.dump(post)})

@posts.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update(id):
    post = Post.find_by_id_secure(id,get_jwt())
    post.message = request.json.get('message',post.message)
    db.session.add(post)
    db.session.commit()    
    return response_with(resp.SUCCESS_200,value={'post':post_schema.dump(post)})


@posts.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete(id):
    post = Post.find_by_id_secure(id,get_jwt())
    db.session.delete(post)
    db.session.commit()
    return response_with(resp.SUCCESS_200,value={'post':post_schema.dump(post)},message="resource deleted")
