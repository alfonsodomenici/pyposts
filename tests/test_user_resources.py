from http import HTTPStatus
from tests.util import create_user,login_user, get_access_token, all_users

def test_create_admin(client,role_admin):
    resp=create_user(client,'admin','admin', role_admin)
    assert resp.status_code==HTTPStatus.CREATED
    assert 'user'in  resp.json
    user=resp.json['user']
    assert user['username']=='admin'
    assert user['role_id']==role_admin.id

def test_login(client,role_admin):
    create_user(client,'admin','admin', role_admin)
    resp=login_user(client,'admin','admin')
    assert resp.status_code==HTTPStatus.CREATED
    assert 'access_token' in resp.json
    token=resp.json['access_token']
    assert token is not None and token != ''

def test_all_success(client,role_admin,role_user):
    create_user(client,'admin','admin', role_admin)
    create_user(client,'user','user', role_user)
    token=get_access_token(client,'admin','admin')
    resp=all_users(client,token)
    assert resp.status_code==HTTPStatus.OK
    assert 'users' in resp.json
    assert len(resp.json)==2



