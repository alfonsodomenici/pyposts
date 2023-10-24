"""Global pytest fixtures."""
import pytest

from app import create_app
from app import db as database
from app.models import User,Role
from flask_jwt_extended import JWTManager
#from tests.util import EMAIL, ADMIN_EMAIL, PASSWORD


@pytest.fixture
def app():
    app = create_app("testing")
    return app

@pytest.fixture
def jwt(app):
    return JWTManager(app)

@pytest.fixture
def db(app, client, request):
    database.drop_all()
    database.create_all()
    database.session.commit()

    def fin():
        database.session.remove()

    request.addfinalizer(fin)
    return database

@pytest.fixture
def role_user(db):
    r = Role(name='USER')
    db.session.add(r)
    db.session.commit()
    return r

@pytest.fixture
def role_admin(db):
    r = Role(name='ADMIN')
    db.session.add(r)
    db.session.commit()
    return r

@pytest.fixture
def admin(db,role_admin):
    user = User(username='admin', password='admin',role=role_admin)
    db.session.add(user)
    db.session.commit()
    return user


@pytest.fixture
def user(db,role_user):
    admin = User(username='user', password='user',role=role_user)
    db.session.add(admin)
    db.session.commit()
    return admin