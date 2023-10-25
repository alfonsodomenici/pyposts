from flask import Blueprint
from app.api.role_resources import roles
from app.api.user_resources import users

api = Blueprint('api',__name__)

api.register_blueprint(roles, url_prefix='/roles')
api.register_blueprint(users, url_prefix='/users')

from app.api import errors