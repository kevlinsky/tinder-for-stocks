from requests import post
from app.main import auth_handler
from test.test_user.test_1_user_signup import user_test_data


user_test_data_not_verified = {'email': 'stttfeerkty7@neaeo.com', 'password': 'pass23', 'first_name': 'Gunaz',
                               'last_name': 'Amirkhanova'}


def test_login_user_not_found():
    response = post('http://web:8000/login', json={"email": "string", "password": "string"})
    assert response.status_code == 200
    assert response.json() == {"status_code": 401, "detail": "User not found", "headers": None}


def test_login_not_verified():
    post('http://web:8000/signup', json=user_test_data_not_verified)
    response = post("http://web:8000/login", json={"email": user_test_data_not_verified["email"], "password":
                                                   user_test_data_not_verified["password"]})
    assert response.status_code == 200
    assert response.json() == {"error": "Verify your email"}


def test_login():
    response = post("http://web:8000/login", json={"email": user_test_data["email"],
                                                   "password": user_test_data["password"]})
    access_token = auth_handler.encode_token(user_test_data['email'])
    refresh_token = auth_handler.encode_refresh_token(user_test_data['email'])
    assert response.status_code == 200
    assert response.json() == {'access_token': access_token, 'refresh_token': refresh_token}


def test_login_invalid_password():
    response = post('http://web:8000/login', json={"email": user_test_data['email'],
                                                   "password": "string"})
    assert response.status_code == 200
    assert response.json() == {"status_code": 401, "detail": "Invalid password", "headers": None}
