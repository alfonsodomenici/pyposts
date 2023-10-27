from flask import Blueprint
from app.api.dommyResources import Dummy,DummyItem
api = Blueprint('api',__name__)

from .postResources import posts
api.register_blueprint(posts, url_prefix='/posts')

from .userResources import users
api.register_blueprint(users, url_prefix='/users', )

from .roleResources import roles
api.register_blueprint(roles, url_prefix='/roles')

from .dommyResources import dummies
api.register_blueprint(dummies,url_prefix='/dummies')
dummies.add_url_rule('', view_func=Dummy.as_view('dummy'))
dummies.add_url_rule('/<int:id>', view_func=DummyItem.as_view('dummyitem'))

from . import  errors