from flask import Blueprint

api = Blueprint('api',__name__)

from .postResources import posts
api.register_blueprint(posts, url_prefix='/posts')

from .userResources import users
api.register_blueprint(users, url_prefix='/users', )

from .roleResources import roles
api.register_blueprint(roles, url_prefix='/roles')

from . import  errors