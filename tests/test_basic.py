from app.models import User,Role

def test_config(app):
    assert app.config['TESTING'] == True

def test_db_defaults(app,db,user,admin,role_user,role_admin):
    assert len(Role.query.all())==2
    assert len(User.query.all())==2

