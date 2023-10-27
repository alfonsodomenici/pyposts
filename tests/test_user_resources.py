import pytest
from http import HTTPStatus
from tests.util import create_user,create_user_with_role_id, login_user, get_access_token, all_users, find_user, update_user, delete_user

def test_create_admin(client,role_admin):
    resp=create_user(client,'admin','admin', role_admin)
    assert resp.status_code==HTTPStatus.CREATED
    assert 'user'in  resp.json
    user=resp.json['user']
    assert user['username']=='admin'
    assert user['role_id']==role_admin.id
        
def test_create_failed(client,role_user):
    resp=create_user(client,'','user', role_user)
    assert resp.status_code==422
    resp=create_user(client,'user','', role_user)
    assert resp.status_code==422
    resp=create_user_with_role_id(client,'user','user', 22)
    assert resp.status_code==422

def test_login(client,role_admin):
    create_user(client,'admin','admin', role_admin)
    resp=login_user(client,'admin','admin')
    assert resp.status_code==HTTPStatus.CREATED
    assert 'access_token' in resp.json
    token=resp.json['access_token']
    assert token is not None and token != ''

def test_all(client,role_admin,role_user):
    create_user(client,'admin','admin', role_admin)
    create_user(client,'user','user', role_user)
    """
    admin call
    """   
    token=get_access_token(client,'admin','admin')
    resp=all_users(client,token)
    assert resp.status_code==HTTPStatus.OK
    assert 'users' in resp.json
    assert len(resp.json)==2

    """
    user call
    """
    token=get_access_token(client,'user','user')
    resp=all_users(client,token)
    assert resp.status_code==HTTPStatus.FORBIDDEN

def test_find(client,role_admin,role_user):
    admin_id=create_user(client,'admin','admin', role_admin).json['user']['id']
    user_id=create_user(client,'user','user', role_user).json['user']['id']
    
    """
    admin call
    """
    token=get_access_token(client,'admin','admin')
    
    resp=find_user(client,admin_id, token)
    assert resp.status_code==HTTPStatus.OK
    assert 'user' in resp.json
    assert resp.json['user']['id']==admin_id

    resp=find_user(client,user_id, token)
    assert resp.status_code==HTTPStatus.OK
    assert 'user' in resp.json
    assert resp.json['user']['id']==user_id   
    
    """
    user call
    """
    token=get_access_token(client,'user','user')
    
    resp=find_user(client,user_id, token)
    assert resp.status_code==HTTPStatus.OK
    assert 'user' in resp.json
    assert resp.json['user']['id']==user_id

    resp=find_user(client,admin_id, token)
    assert resp.status_code==HTTPStatus.FORBIDDEN

def test_update(client,role_admin,role_user):
    admin_id=create_user(client,'admin','admin', role_admin).json['user']['id']
    user_id=create_user(client,'user','user', role_user).json['user']['id']

    """
    admin call
    """
    token=get_access_token(client,'admin','admin')
    
    resp=update_user(client,admin_id, token,'adminadmin')
    assert resp.status_code==HTTPStatus.OK
    assert 'user' in resp.json
    assert resp.json['user']['username']=='adminadmin' 
    
    """
    user call
    """
    token=get_access_token(client,'user','user')
    
    resp=update_user(client,user_id, token,'useruser')
    assert resp.status_code==HTTPStatus.OK
    assert 'user' in resp.json
    assert resp.json['user']['username']=='useruser'

    resp=update_user(client,admin_id, token, 'admin-----')
    assert resp.status_code==HTTPStatus.FORBIDDEN

def test_delete(client, role_admin,role_user):
    admin_id=create_user(client,'admin','admin', role_admin).json['user']['id']
    user_id=create_user(client,'user','user', role_user).json['user']['id']
    maria_id=create_user(client,'maria','maria', role_user).json['user']['id']
    """
    admin call
    """
    token=get_access_token(client,'admin','admin')
    
    resp=delete_user(client,maria_id, token)
    assert resp.status_code==HTTPStatus.NO_CONTENT
    
    """
    user call
    """
    maria_id=create_user(client,'maria','maria', role_user).json['user']['id']
    token=get_access_token(client,'user','user')
    
    resp=delete_user(client,maria_id, token)
    assert resp.status_code==HTTPStatus.FORBIDDEN
