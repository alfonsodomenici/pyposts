from flask import Blueprint
from app.api.role_resources import roles
from app.api.user_resources import users
from app.api.post_resources import posts

api = Blueprint('api',__name__)

api.register_blueprint(roles, url_prefix='/roles')
api.register_blueprint(users, url_prefix='/users')
api.register_blueprint(posts,url_prefix='/posts')

from app.api import errors