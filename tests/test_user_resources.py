from util import login_user, create_user, all_users, find_user
from http import HTTPStatus

def test_create_user_admin(client,role_admin):
    resp=create_user(client,'admin','admin',role_admin)
    assert resp.status_code == HTTPStatus.CREATED
    assert 'user' in resp.json
    user = resp.json['user']
    assert user['username'] == 'admin'
    assert user['role_id'] == role_admin.id

def test_login(client,app, jwt, role_admin):
    create_user(client,'admin','admin',role_admin)
    resp=login_user(client,'admin','admin')
    assert resp.status_code == HTTPStatus.CREATED
    assert 'access_token' in resp.json

def test_all_users(client,app, jwt, role_admin, role_user):
    create_user(client,'admin','admin',role_admin)
    create_user(client,'user','user',role_user)
    resp=login_user(client,'admin','admin')
    token=resp.json['access_token']
    assert token is not None and token is not ''
    resp=all_users(client,token)
    assert resp.status_code == HTTPStatus.OK
    assert 'users' in resp.json
    users = resp.json['users']
    assert len(users)==2

def test_all_users_forbidden(client,app, jwt, role_admin, role_user):
    create_user(client,'admin','admin',role_admin)
    create_user(client,'user','user',role_user)
    resp=login_user(client,'user','user')
    token=resp.json['access_token']
    assert token is not None and token is not ''
    resp=all_users(client,token)
    assert resp.status_code == HTTPStatus.FORBIDDEN

def test_find_user(client,app, jwt, role_admin, role_user):
    admin_id=create_user(client,'admin','admin',role_admin).json['user']['id']
    user_id=create_user(client,'user','user',role_user).json['user']['id']
    resp=login_user(client,'user','user')
    token=resp.json['access_token']
    assert token is not None and token is not ''
    resp=find_user(client,token,user_id)
    assert resp.status_code == HTTPStatus.OK