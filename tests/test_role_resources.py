from http import HTTPStatus
from tests.util import create_user,get_access_token, all_roles,create_role, find_role, update_role, delete_role

def test_all(client, role_admin, role_user):
    create_user(client,'admin','admin', role_admin)
    create_user(client,'user','user', role_user)
    """
    admin calls
    """
    token = get_access_token(client,'admin','admin')
    resp=all_roles(client,token)
    assert resp.status_code==HTTPStatus.OK
    assert 'roles' in resp.json
    assert len(resp.json['roles'])==2

    """
    user calls
    """
    token = get_access_token(client,'user','user')
    resp=all_roles(client,token)
    assert resp.status_code==HTTPStatus.FORBIDDEN

def test_create(client,role_admin, role_user):
    """
    admin
    """
    create_user(client,'admin','admin', role_admin)
    create_user(client,'user','user', role_user)
    token = get_access_token(client,'admin','admin')
    resp=create_role(client,token,'DEV')
    assert resp.status_code==HTTPStatus.CREATED
    assert 'role' in resp.json
    assert resp.json['role']['name']=='DEV'
    """
    user
    """
    token = get_access_token(client,'user','user')
    resp=create_role(client,token,'DEV-DEV')
    assert resp.status_code==HTTPStatus.FORBIDDEN   

def test_create_failed(client, role_admin):
    create_user(client,'admin','admin', role_admin)
    token = get_access_token(client,'admin','admin')
    resp=create_role(client,token,'')
    assert resp.status_code==422

def test_find(client,role_admin, role_user):
    """
    admin
    """
    create_user(client,'admin','admin', role_admin)
    create_user(client,'user','user', role_user)
    token = get_access_token(client,'admin','admin')
    resp=find_role(client,role_user.id,token)
    assert resp.status_code==HTTPStatus.OK
    assert 'role' in resp.json
    assert resp.json['role']['name']==role_user.name
    """
    user
    """
    token = get_access_token(client,'user','user')
    resp=find_role(client,role_user.id,token)
    assert resp.status_code==HTTPStatus.FORBIDDEN   

def test_update(client,role_admin, role_user):
    """
    admin
    """
    create_user(client,'admin','admin', role_admin)
    create_user(client,'user','user', role_user)
    token = get_access_token(client,'admin','admin')
    dev_id=create_role(client,token,'DEV').json['role']['id']
    resp=update_role(client,dev_id,token,'DEV-DEV')
    assert resp.status_code==HTTPStatus.OK
    assert 'role' in resp.json
    assert resp.json['role']['name']=='DEV-DEV'
    """
    user
    """
    token = get_access_token(client,'user','user')
    resp=update_role(client,dev_id,token,'DEV-DEV')
    assert resp.status_code==HTTPStatus.FORBIDDEN   

def test_delete(client,role_admin, role_user):
    """
    admin
    """
    create_user(client,'admin','admin', role_admin)
    create_user(client,'user','user', role_user)
    token = get_access_token(client,'admin','admin')
    dev_id=create_role(client,token,'DEV').json['role']['id']
    resp=delete_role(client,dev_id,token)
    assert resp.status_code==HTTPStatus.NO_CONTENT

    dev_id=create_role(client,token,'DEV').json['role']['id']

    """
    user
    """
    token = get_access_token(client,'user','user')
    resp=delete_role(client,dev_id,token)
    assert resp.status_code==HTTPStatus.FORBIDDEN   