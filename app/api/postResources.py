from flask import request, current_app
from flask_jwt_extended import jwt_required, current_user
from .decorators import admin_required
from .responses import response_with
from . import responses as resp
from . import api
from ..models import Post
from app import db

@api.route('/posts')
@jwt_required()
def all_posts():
    posts = Post.query.all() if current_user.is_admin() else Post.find_by_user_id(current_user.id)
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
    data = request.get_json()
    current_app.logger.info(data)
    post = Post.from_json(data)
    post.user_id=current_user.id
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

def _check_and_find_post(id):
    post = Post.query.get_or_404(id)
    if post.user_id!=current_user.id and not current_user.is_admin():
        return 'unautorized',401
    return post