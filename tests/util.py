
from flask import url_for
import logging

def create_user(test_client,usr,pwd,role):
    return test_client.post(
        url_for("api.create_user"),json={
            'username':usr,
            'password':pwd,
            'role_id': role.id
        })    

def login_user(test_client,usr,pwd):
    return test_client.post(
        url_for("api.user_login"),json={
            'username':usr,
            'password':pwd
        })

def all_users(test_client, access_token):
    return test_client.get(
        url_for("api.all_users"), headers={"Authorization": f"Bearer {access_token}"}
    )

def find_user(test_client, access_token,user_id):
    return test_client.get(
        url_for("api.find_user",id=user_id), headers={"Authorization": f"Bearer {access_token}"}
    )