import pytest
from app import create_app
from app import db as database
from app.models.role import Role

@pytest.fixture()
def app():
    application=create_app('testing')
    return application

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def db(app,request):
    database.drop_all()
    database.create_all()
    database.session.commit()

    def fin():
        database.session.remove()

    request.addfinalizer(fin)

    return database

@pytest.fixture()
def role_user(db):
    r = Role(name='USER')
    db.session.add(r)
    db.session.commit()
    return r

@pytest.fixture()
def role_admin(db):
    r = Role(name='ADMIN')
    db.session.add(r)
    db.session.commit()
    return r

