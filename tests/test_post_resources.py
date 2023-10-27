from http import HTTPStatus
from tests.util import create_user,get_access_token, all_posts,create_post,find_post,update_post,delete_post

def test_all(client,role_admin,role_user):
    create_user(client,'admin','admin', role_admin)
    create_user(client,'user','user', role_user)
    """
    admin calls
    """
    token = get_access_token(client,'admin','admin')
    resp=all_posts(client,token)
    assert resp.status_code==HTTPStatus.OK
    assert 'posts' in resp.json
    assert len(resp.json['posts'])==0
    resp=create_post(client,token,'admin post')
    resp=all_posts(client,token)
    assert len(resp.json['posts'])==1

    """
    user calls
    """
    token = get_access_token(client,'user','user')
    resp=all_posts(client,token)
    assert resp.status_code==HTTPStatus.OK
    assert 'posts' in resp.json
    assert len(resp.json['posts'])==0
    resp=create_post(client,token,'user post')
    resp=all_posts(client,token)
    assert len(resp.json['posts'])==1

    """
    admin 
    """
    token = get_access_token(client,'admin','admin')
    resp=all_posts(client,token)
    assert len(resp.json['posts'])==2

def test_create(client,role_admin,role_user):
    admin_id=create_user(client,'admin','admin', role_admin).json['user']['id']
    user_id=create_user(client,'user','user', role_user).json['user']['id']
    """
    admin calls
    """
    token = get_access_token(client,'admin','admin')
    resp=create_post(client,token,'admin post')
    assert resp.status_code==HTTPStatus.CREATED
    assert 'post' in resp.json
    assert resp.json['post']['message']=='admin post'
    assert resp.json['post']['user_id']==admin_id

    """
    user calls
    """
    token = get_access_token(client,'user','user')
    resp=create_post(client,token,'user post')
    assert resp.status_code==HTTPStatus.CREATED
    assert 'post' in resp.json
    assert resp.json['post']['message']=='user post'
    assert resp.json['post']['user_id']==user_id 

def test_create_failed(client, role_admin):
    create_user(client,'admin','admin', role_admin)
    token = get_access_token(client,'admin','admin')
    resp=create_post(client,token,'')
    assert resp.status_code==422

def test_find(client,role_admin,role_user):
    admin_id=create_user(client,'admin','admin', role_admin).json['user']['id']
    user_id=create_user(client,'user','user', role_user).json['user']['id']
    
    """
    admin call
    """
    token=get_access_token(client,'admin','admin')
    admin_post_id=create_post(client,token,'admin post').json['post']['id']
    resp=find_post(client,admin_post_id, token)
    assert resp.status_code==HTTPStatus.OK
    assert 'post' in resp.json
    assert resp.json['post']['id']==admin_post_id
    assert resp.json['post']['message']=='admin post'
    assert resp.json['post']['user_id']==admin_id

    """
    user calls
    """
    token=get_access_token(client,'user','user')
    user_post_id=create_post(client,token,'user post').json['post']['id']
    resp=find_post(client,user_post_id, token)
    assert resp.status_code==HTTPStatus.OK
    assert 'post' in resp.json
    assert resp.json['post']['id']==user_post_id

    resp=find_post(client,admin_post_id, token)
    assert resp.status_code==HTTPStatus.FORBIDDEN

    """
    admin
    """
    token=get_access_token(client,'admin','admin')
    resp=find_post(client,user_post_id, token)
    assert resp.status_code==HTTPStatus.OK 

def test_update(client,role_admin,role_user):
    admin_id=create_user(client,'admin','admin', role_admin).json['user']['id']
    user_id=create_user(client,'user','user', role_user).json['user']['id']

    """
    admin call
    """
    token=get_access_token(client,'admin','admin')
    admin_post_id=create_post(client,token,'admin post').json['post']['id']
    resp=update_post(client,admin_post_id, token,'admin post updated')
    assert resp.status_code==HTTPStatus.OK
    assert 'post' in resp.json
    assert resp.json['post']['message']=='admin post updated'
    assert resp.json['post']['user_id']==admin_id

    """
    user calls
    """
    token=get_access_token(client,'user','user')
    user_post_id=create_post(client,token,'user post').json['post']['id']
    resp=update_post(client,user_post_id, token,'user post updated')
    assert resp.status_code==HTTPStatus.OK
    assert 'post' in resp.json
    assert resp.json['post']['message']=='user post updated'
    assert resp.json['post']['user_id']==user_id
 
    """
    admin
    """
    token=get_access_token(client,'admin','admin')
    resp=update_post(client,user_post_id, token,'user post updated by admin')
    assert resp.status_code==HTTPStatus.OK
    assert 'post' in resp.json
    assert resp.json['post']['message']=='user post updated by admin'
    assert resp.json['post']['user_id']==user_id   

def test_delete(client,role_admin,role_user):
    admin_id=create_user(client,'admin','admin', role_admin).json['user']['id']
    user_id=create_user(client,'user','user', role_user).json['user']['id']
    
    """
    admin call
    """
    token=get_access_token(client,'admin','admin')
    admin_post_id=create_post(client,token,'admin post').json['post']['id']
    resp=delete_post(client,admin_post_id, token)
    assert resp.status_code==HTTPStatus.NO_CONTENT

    admin_post_id=create_post(client,token,'admin post').json['post']['id']

    """
    user calls
    """
    token=get_access_token(client,'user','user')
    user_post_id=create_post(client,token,'user post').json['post']['id']
    resp=delete_post(client,user_post_id, token)
    assert resp.status_code==HTTPStatus.NO_CONTENT

    resp=delete_post(client,admin_post_id, token)
    assert resp.status_code==HTTPStatus.FORBIDDEN  


    user_post_id=create_post(client,token,'user post').json['post']['id']   

    """
    admin
    """
    token=get_access_token(client,'admin','admin')
    resp=delete_post(client,user_post_id, token)
    assert resp.status_code==HTTPStatus.NO_CONTENT