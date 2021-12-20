import asyncio
import aiopg
from requests import post, get

from app.main import auth_handler
from test.test_user.test_data import server_path, password_reset_user_test_data
import time
import os


def test_password_reset_request():
    post(server_path + '/signup', json=password_reset_user_test_data)
    user_email = password_reset_user_test_data['email']
    user_hash = auth_handler.encode_confirm_token(user_email)
    get(server_path + f'/email-confirm/{user_hash}')
    response = post(server_path + '/password-reset/request', json={"email": password_reset_user_test_data['email']})
    assert response.status_code == 200
    assert response.json() == {'message': 'Reset code was sent on specified email'}


def test_password_reset_request_user_not_found():
    response = post(server_path + '/password-reset/request', json={"email": "not_found_email@gmail.com"})
    assert response.status_code == 200
    assert response.json() == {"status_code": 401, "detail": "User not found", "headers": None}


time.sleep(60)


async def get_reset_code():
    conn = await aiopg.connect(database=os.getenv('POSTGRES_DB'), host=os.getenv('POSTGRES_HOST'),
                               user=os.getenv('POSTGRES_USER'), password=os.getenv('POSTGRES_PASSWORD'),
                               port=os.getenv('POSTGRES_PORT'))
    cursor = await conn.cursor()
    await cursor.execute('SELECT * FROM users_codes WHERE id=(SELECT max(id) FROM users_codes) ')
    reset_code = await cursor.fetchone()
    await conn.close()
    print(reset_code[2])
    return reset_code[2]


def test_password_reset():
    response = post(server_path + '/password-reset/', json={"email": password_reset_user_test_data['email'],
                                                             "code": asyncio.run(get_reset_code()),
                                                             "new_password": 'newpass'})
    assert response.status_code == 200
    assert response.json() == {'message': 'Password was changed successfully'}
