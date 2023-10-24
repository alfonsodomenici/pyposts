from app.models import User,Role

def test_config(app):
    assert app.config['TESTING'] == True

def test_db_defaults(app,db,role_user,role_admin):
    assert len(Role.query.all())==2

