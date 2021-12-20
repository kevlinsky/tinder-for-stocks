from requests import get, post
from app.main import auth_handler
from test.test_user.test_data import server_path, confirm_user_test_data


def test_confirm_email():
    post(server_path + '/signup', json=confirm_user_test_data)
    user_email = confirm_user_test_data['email']
    user_hash = auth_handler.encode_confirm_token(user_email)
    response = get(server_path + f'/email-confirm/{user_hash}')
    assert response.status_code == 200
    assert response.json() == {"message": f"Email {user_email} successfully confirmed"}


def test_confirm_invalid_token():
    response = get(server_path + '/email-confirm/fake-token')
    assert response.json() == {"detail": "Invalid token"}
