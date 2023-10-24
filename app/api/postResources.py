from flask import request, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from .decorators import admin_required
from .responses import response_with
from . import responses as resp
from . import api
from ..models import Post,User
from app import db

@api.route('/posts')
@jwt_required()
def all_posts():
    logged = logged_user()
    posts = Post.query.all() if logged.is_admin() else Post.find_by_user_id(logged.id)
    result = [post.to_json() for post in posts]
    return response_with(resp.SUCCESS_200,value={'posts':result}) 

@api.route('/posts/<int:id>')
@jwt_required()
def find_post(id):
    post=_check_and_find_post(id)
    return response_with(resp.SUCCESS_200,value={'post':post.to_json()})


@api.route('/posts', methods=['POST'])
@jwt_required()
def create_post():
    logged = logged_user()
    data = request.get_json()
    current_app.logger.info(data)
    post = Post.from_json(data)
    post.user_id=logged.id
    db.session.add(post)
    db.session.commit()
    return response_with(resp.SUCCESS_201,value={'post':post.to_json()})

@api.route('/posts/<int:id>', methods=['PUT'])
@jwt_required()
def update_post(id):
    post = _check_and_find_post(id)
    post.message = request.json.get('message',post.message)
    db.session.add(post)
    db.session.commit()    
    return response_with(resp.SUCCESS_200,value={'post':post.to_json()})


@api.route('/posts/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_post(id):
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
        return 'unautorized',401
    return post