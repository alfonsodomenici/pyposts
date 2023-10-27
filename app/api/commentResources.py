from flask.views import MethodView


class Comment(MethodView):
    def get(self):
        return 'all'
    def post(self):
        return 'post'   

class CommentItem(MethodView):
    def get(self,id):
        return 'item with id'
    
    def put(self,id):
        return 'update item with id'
    
    def delete(self,id):
        return 'delete item with id'