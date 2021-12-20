from requests import get, post
import aiopg
import asyncio
import os
import random
import string

from app.main import auth_handler
from screener.filter import filter_stocks
from screener.models import Screener
from user.models import User
from test.test_data import test_screener_data, test_user_screener_data, server_path

path = 'http://web:8080/screener/'


def create_access_token():
    post(server_path + '/signup', json=test_user_screener_data)
    user_email = test_user_screener_data['email']
    user_hash = auth_handler.encode_confirm_token(user_email)
    get(server_path + f'/email-confirm/{user_hash}')
    access_token = auth_handler.encode_token(test_user_screener_data['email'])
    return access_token


test_token = create_access_token()


async def get_screener_id():
    conn = await aiopg.connect(database=os.getenv('POSTGRES_DB'), host=os.getenv('POSTGRES_HOST'),
                               user=os.getenv('POSTGRES_USER'), password=os.getenv('POSTGRES_PASSWORD'),
                               port=os.getenv('POSTGRES_PORT'))
    cursor = await conn.cursor()
    await cursor.execute('SELECT max(id) FROM screeners')
    max_id_tuple = await cursor.fetchone()
    if max_id_tuple:
        max_id = max_id_tuple[0]
    else:
        max_id = 1
    await conn.close()
    return max_id


async def create_screener():
    response = post(path, json=test_screener_data, headers={"Authorization": "Bearer" + test_token})
    screener_id = response.json()['id']
    return await Screener.get(screener_id)


def test_create_screener():
    response = post(path, json=test_screener_data, headers={"Authorization": "Bearer" + test_token})
    assert response.status_code == 200
    assert response.json() == {'id': asyncio.run(get_screener_id()), "message": "screener was successfully created"}


async def test_get_screeners():
    response = get(path, headers={"Authorization": "Bearer" + test_token})
    email = auth_handler.decode_token(test_token)
    user = await User.get_by_email(email)
    screeners = await Screener.get_user_screeners(user.id)
    assert response.status_code == 200
    assert response.json() == screeners


async def test_run_screener():
    screener = create_screener()
    response = get(path + screener.id, headers={"Authorization": "Bearer" + test_token})
    result = await filter_stocks(screener)
    assert response.status_code == 200
    assert response.json() == result
