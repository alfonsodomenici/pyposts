from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt
from app.models.post import Post
from app.api.responses import response_with
from app.api import responses as resp
from app import db
from app.models.schemas import post_schema,posts_schema

posts = Blueprint('posts',__name__)

@posts.route('')
@jwt_required()
def all():
    claims=get_jwt()
    result = Post.query.all() if claims.get('role')=='ADMIN' else Post.find_by_user_id(claims.get('sub_id'))
    return response_with(resp.SUCCESS_200,{'posts':posts_schema.dump(result)})

@posts.route('', methods=['POST'])
@jwt_required()
def create():
    json = request.get_json()
    post = post_schema.load(json)
    claims=get_jwt()
    post.user_id=claims['sub_id']
    db.session.add(post)
    db.session.commit()
    return response_with(resp.SUCCESS_201,{'post':post_schema.dump(post)})

@posts.route('/<int:id>')
@jwt_required()
def find(id):
    post=Post.find_by_id_secure(id,get_jwt())
    return response_with(resp.SUCCESS_200, {'post':post_schema.dump(post)})

@posts.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update(id):
    json=request.get_json()
    post=Post.find_by_id_secure(id,get_jwt())
    post.message=json.get('message',post.message)
    db.session.add(post)
    db.session.commit()
    return response_with(resp.SUCCESS_200, {'post':post_schema.dump(post)})

@posts.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete(id):
    post = Post.find_by_id_secure(id,get_jwt())
    db.session.delete(post)
    db.session.commit()
    return response_with(resp.SUCCESS_204)