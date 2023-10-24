from flask import request, current_app, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from .decorators import admin_required
from .responses import response_with
from . import responses as resp
from . import api
from app.models.user import User
from app.models.post import Post
from app import db
from app.exceptions import NotResourceOwnerError

posts = Blueprint('posts',__name__)

@posts.route('/')
@jwt_required()
def all():
    logged = logged_user()
    posts = Post.query.all() if logged.is_admin() else Post.find_by_user_id(logged.id)
    result = [post.to_json() for post in posts]
    return response_with(resp.SUCCESS_200,value={'posts':result}) 

@posts.route('/<int:id>')
@jwt_required()
def find(id):
    post=_check_and_find_post(id)
    return response_with(resp.SUCCESS_200,value={'post':post.to_json()})


@posts.route('/', methods=['POST'])
@jwt_required()
def create():
    logged = logged_user()
    data = request.get_json()
    current_app.logger.info(data)
    post = Post.from_json(data)
    post.user_id=logged.id
    db.session.add(post)
    db.session.commit()
    return response_with(resp.SUCCESS_201,value={'post':post.to_json()})

@posts.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update(id):
    post = _check_and_find_post(id)
    post.message = request.json.get('message',post.message)
    db.session.add(post)
    db.session.commit()    
    return response_with(resp.SUCCESS_200,value={'post':post.to_json()})


@posts.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete(id):
    post = _check_and_find_post(id)
    db.session.delete(post)
    db.session.commit()
    return response_with(resp.SUCCESS_204)

def logged_user():
    identity = get_jwt_identity()
    return User.find_by_username(identity)

def _check_and_find_post(id):
    logged = logged_user()
    post = db.get_or_404(Post,id)
    if post.user_id!=logged.id and not logged.is_admin():
        raise NotResourceOwnerError('id non corrispondente')
    return post