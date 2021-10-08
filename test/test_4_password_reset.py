import asyncio
import aiopg
from requests import post
from .test_1_user_signup import user_test_data
import time

email_not_found = "notfound@gmail.com"


def test_password_reset_request():
    response = post('http://web:8000/password-reset/request', json={"email": user_test_data['email']})
    assert response.status_code == 200
    assert response.json() == {'message': 'Reset code was sent on specified email'}


def test_password_reset_request_user_not_found():
    response = post('http://web:8000/password-reset/request', json={"email": email_not_found})
    assert response.status_code == 200
    assert response.json() == {"status_code": 401, "detail": "User not found", "headers": None}


time.sleep(60)


async def get_reset_code():
    conn = await aiopg.connect(database="tinder", host="db", user="tinder", password="tinder", port=5432)
    cursor = await conn.cursor()
    await cursor.execute('SELECT * FROM users_codes WHERE id=(SELECT max(id) FROM users_codes) ')
    reset_code = await cursor.fetchone()
    await conn.close()
    print(reset_code[2])
    return reset_code[2]


def test_password_reset():
    response = post('http://web:8000/password-reset/', json={"email": user_test_data['email'],
                                                             "code": asyncio.run(get_reset_code()),
                                                             "new_password": 'newpass'})
    assert response.status_code == 200
    assert response.json() == {'message': 'Password was changed successfully'}




