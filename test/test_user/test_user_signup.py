import aiopg
import asyncio
from requests import get, post
import os
from test.test_data import server_path, signup_user_test_data, signup_user_test_invalid_data


async def get_user_id():
    conn = await aiopg.connect(database=os.getenv('POSTGRES_DB'), host=os.getenv('POSTGRES_HOST'),
                               user=os.getenv('POSTGRES_USER'), password=os.getenv('POSTGRES_PASSWORD'),
                               port=os.getenv('POSTGRES_PORT'))
    cursor = await conn.cursor()
    await cursor.execute('SELECT max(id) FROM users')
    max_id_tuple = await cursor.fetchone()
    if max_id_tuple:
        max_id = max_id_tuple[0]
    else:
        max_id = 1
    await conn.close()
    return max_id


async def get_existed_user_data():
    conn = await aiopg.connect(database=os.getenv('POSTGRES_DB'), host=os.getenv('POSTGRES_HOST'),
                               user=os.getenv('POSTGRES_USER'), password=os.getenv('POSTGRES_PASSWORD'),
                               port=os.getenv('POSTGRES_PORT'))
    cursor = await conn.cursor()
    await cursor.execute('SELECT * FROM users')
    user_exists = await cursor.fetchone()
    user_exists_data = {'email': user_exists[3], 'password': 'password', 'first_name': user_exists[1],
                        'last_name': user_exists[2]}
    await conn.close()
    return user_exists_data


def test_index():
    response = get(server_path + '/')
    assert response.status_code == 200
    assert response.json() == {"hello": "world"}


def test_signup():
    response = post(server_path + '/signup', json=signup_user_test_data)
    assert response.status_code == 200
    assert response.json() == {"id": asyncio.run(get_user_id()),
                               'message': 'Link for email verification was sent to specified email address'}


def test_signup_already_exists():
    response = post(server_path + '/signup', json=asyncio.run(get_existed_user_data()))
    assert response.status_code == 200
    assert response.json() == {"error": "Account already exists"}


def test_signup_invalid_email():
    response = post(server_path + '/signup', json=signup_user_test_invalid_data)
    assert response.status_code == 422
    assert response.json() == {'detail': [{'loc': ['body', 'email'], 'msg': 'value is not a valid email address',
                                           'type': 'value_error.email'}]}
