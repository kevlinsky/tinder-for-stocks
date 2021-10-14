from requests import post, get
from app.main import auth_handler
from .test_1_user_signup import user_test_data


def test_confirm_email():
    user_email = user_test_data['email']
    user_hash = auth_handler.encode_confirm_token(user_email)
    response = get(f'http://web:8000/email-confirm/{user_hash}')
    assert response.status_code == 200
    assert response.json() == {"message": f"Email {user_email} successfully confirmed"}


def test_confirm_invalid_token():
    response = get('http://web:8000/email-confirm/fake-token')
    assert response.json() == {"detail": "Invalid token"}

