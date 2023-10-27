from flask import Blueprint
from .commentResources import CommentItem, Comment

api = Blueprint('api',__name__)
api.add_url_rule('/comments', view_func=Comment.as_view('comment'))
api.add_url_rule('/comments/<int:id>', view_func=CommentItem.as_view('comment_item'))

from .postResources import posts
api.register_blueprint(posts, url_prefix='/posts')

from .userResources import users
api.register_blueprint(users, url_prefix='/users', )

from .roleResources import roles
api.register_blueprint(roles, url_prefix='/roles')

from .dummyResources import dummies
api.register_blueprint(dummies,url_prefix='/dummies')


from . import  errors
