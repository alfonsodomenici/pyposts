from flask import url_for

def create_user(test_client,usr,pwd,role):
    return test_client.post(
        url_for('api.users.create'),json={
            'username':usr,
            'password':pwd,
            'role_id': role.id
        }
    )

def create_user_with_role_id(test_client,usr,pwd,role_id):
    return test_client.post(
        url_for('api.users.create'),json={
            'username':usr,
            'password':pwd,
            'role_id': role_id
        }
    )

def login_user(test_client,usr,pwd):
    return test_client.post(
        url_for('api.users.login'),json={
            'username':usr,
            'password':pwd
        })

def get_access_token(test_client,usr,pwd):
    resp=login_user(test_client,usr,pwd)
    return resp.json['access_token']

"""
users util
"""
def all_users(test_client,token):
    return test_client.get(
        url_for('api.users.all'), headers={"Authorization": f"Bearer {token}"}
    )

def find_user(test_client,user_id,token):
    return test_client.get(
        url_for('api.users.find',id=user_id), headers={"Authorization": f"Bearer {token}"}
    )

def update_user(test_client,user_id,token,username):
    return test_client.put(
        url_for('api.users.update',id=user_id), headers={"Authorization": f"Bearer {token}"}, json={
            'username':username
        }
    )

def delete_user(test_client,user_id,token):
    return test_client.delete(
        url_for('api.users.delete',id=user_id), headers={"Authorization": f"Bearer {token}"}
    )

"""
roles util
"""

def create_role(test_client,token,name):
    return test_client.post(
        url_for('api.roles.create'),json={
            'name':name
        }, headers={"Authorization": f"Bearer {token}"}
    )

def all_roles(test_client,token):
    return test_client.get(
        url_for('api.roles.all'), headers={"Authorization": f"Bearer {token}"}
    )

def find_role(test_client,role_id,token):
    return test_client.get(
        url_for('api.roles.find',id=role_id), headers={"Authorization": f"Bearer {token}"}
    )

def update_role(test_client,role_id,token,name):
    return test_client.put(
        url_for('api.roles.update',id=role_id), headers={"Authorization": f"Bearer {token}"}, json={
            'name':name
        }
    )

def delete_role(test_client,role_id,token):
    return test_client.delete(
        url_for('api.roles.delete',id=role_id), headers={"Authorization": f"Bearer {token}"}
    )

"""
posts util
"""
def create_post(test_client,token,message):
    return test_client.post(
        url_for('api.posts.create'),json={
            'message':message
        }, headers={"Authorization": f"Bearer {token}"}
    )

def all_posts(test_client,token):
    return test_client.get(
        url_for('api.posts.all'), headers={"Authorization": f"Bearer {token}"}
    )

def find_post(test_client,post_id,token):
    return test_client.get(
        url_for('api.posts.find',id=post_id), headers={"Authorization": f"Bearer {token}"}
    )

def update_post(test_client,post_id,token,message):
    return test_client.put(
        url_for('api.posts.update',id=post_id), headers={"Authorization": f"Bearer {token}"}, json={
            'message':message
        }
    )

def delete_post(test_client,post_id,token):
    return test_client.delete(
        url_for('api.posts.delete',id=post_id), headers={"Authorization": f"Bearer {token}"}
    )