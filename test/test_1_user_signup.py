import aiopg
import asyncio
from requests import get, post


def test_index():
    response = get("http://web:8000/")
    assert response.status_code == 200
    assert response.json() == {"hello": "world"}


user_test_data = {'email': 'sensitizers@gemuk.buzz', 'password': 'pass23', 'first_name': 'Gunaz',
                  'last_name': 'Amirkhanova'}


async def get_user_id():
    conn = await aiopg.connect(database="tinder", host="db", user="tinder", password="tinder", port=5432)
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
    conn = await aiopg.connect(database="tinder", host="db", user="tinder", password="tinder", port=5432)
    cursor = await conn.cursor()
    await cursor.execute('SELECT * FROM users')
    user_exists = await cursor.fetchone()
    user_exists_data = {'email': user_exists[3], 'password': 'password', 'first_name': user_exists[1], 'last_name': user_exists[2]}
    await conn.close()
    return user_exists_data


def test_signup():
    response = post('http://web:8000/signup', json=user_test_data)
    assert response.status_code == 200
    assert response.json() == {"id": asyncio.run(get_user_id()), "message": "Verification code was sent to the specified email"}


def test_signup_already_exists():
    response = post('http://web:8000/signup', json=asyncio.run(get_existed_user_data()))
    assert response.status_code == 200
    assert response.json() == {"error": "Account already exists"}


user_test_data_invalid_email = {'email': 'mrrrrrrrrrr', 'password': 'pass23', 'first_name': 'Gunaz',
                  'last_name': 'Amirkhanova'}


def test_signup_invalid_email():
    response = post('http://web:8000/signup', json=user_test_data_invalid_email)
    assert response.status_code == 422
    assert response.json() == {'detail': [{'loc': ['body', 'email'], 'msg': 'value is not a valid email address',
                                           'type': 'value_error.email'}]}





