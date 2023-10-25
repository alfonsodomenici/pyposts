from app.api import api

@api.route('/roles')
def all():
    return 'all'

