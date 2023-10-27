from flask import Blueprint
from flask.views import MethodView

dummies = Blueprint('dummies',__name__)

class Dummy(MethodView):
    def get(self):
        return 'all'
    def post(self):
        return 'post'   
    
class DummyItem(MethodView):
    def get(self,id):
        return 'item with id'
    
    def put(self,id):
        return 'update item with id'
    
    def delete(self,id):
        return 'delete item with id'
