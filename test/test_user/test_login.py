from requests import post, get
from app.main import auth_handler
from test.test_data import server_path, login_user_test_data_not_verified, login_user_test_data


def test_login_user_not_found():
    response = post(server_path + '/login', json={"email": "not_found", "password": "not_found"})
    assert response.status_code == 200
    assert response.json() == {"status_code": 401, "detail": "User not found", "headers": None}


def test_login_not_verified():
    post(server_path + '/signup', json=login_user_test_data_not_verified)
    response = post(server_path + "/login", json={"email": login_user_test_data_not_verified["email"],
                                                  "password": login_user_test_data_not_verified["password"]})
    assert response.status_code == 200
    assert response.json() == {"error": "Verify your email"}


def test_login():
    post(server_path + '/signup', json=login_user_test_data)
    user_email = login_user_test_data['email']
    user_hash = auth_handler.encode_confirm_token(user_email)
    get(server_path + f'/email-confirm/{user_hash}')
    response = post(server_path + "/login", json={"email": login_user_test_data["email"],
                                                  "password": login_user_test_data["password"]})
    access_token = auth_handler.encode_token(login_user_test_data['email'])
    refresh_token = auth_handler.encode_refresh_token(login_user_test_data['email'])
    assert response.status_code == 200
    assert response.json() == {'access_token': access_token, 'refresh_token': refresh_token}


def test_login_invalid_password():
    response = post(server_path + '/login', json={"email": login_user_test_data['email'],
                                                  "password": "wrong_password"})
    assert response.status_code == 200
    assert response.json() == {"status_code": 401, "detail": "Invalid password", "headers": None}
