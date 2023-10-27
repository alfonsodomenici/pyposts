from app.models.role import Role

def test_app_config(app):
    assert app.config['TESTING'] == True

def test_default_roles(role_user, role_admin):
    assert len(Role.query.all())==2