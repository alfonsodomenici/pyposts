from flask import url_for

def create_user(test_client,usr,pwd,role):
    return test_client.post(
        url_for('api.users.create'),json={
            'username':usr,
            'password':pwd,
            'role_id': role.id
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

def all_users(test_client,token):
    return test_client.get(
        url_for('api.users.all'), headers={"Authorization": f"Bearer {token}"}
    )