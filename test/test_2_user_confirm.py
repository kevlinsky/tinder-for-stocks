import aiopg
import asyncio
from requests import post


async def get_users_code():

    conn = await aiopg.connect(database="tinder", host="db", user="tinder", password="tinder", port=5432)
    cursor = await conn.cursor()
    await cursor.execute('SELECT * FROM users WHERE id=(SELECT max(id) FROM users)')
    user_email = await cursor.fetchone()
    await conn.close()
    conn = await aiopg.connect(database="tinder", host="db", user="tinder", password="tinder", port=5432)
    cursor = await conn.cursor()
    await cursor.execute('SELECT * FROM users_codes WHERE id=(SELECT max(id) FROM users_codes)')
    user_code = await cursor.fetchone()
    await conn.close()
    return {"email": user_email[3], "code": user_code[2]}


def test_confirm_email_wrong_code():
    email_code = asyncio.run(get_users_code())
    wrong_code = {"email": email_code["email"], 'code': 0}
    response = post('http://web:8000/signup/email-confirm', json=wrong_code)
    assert response.status_code == 200
    assert response.json() == {"error": "Wrong code for specified user"}


def test_confirm_email():
    email_code = asyncio.run(get_users_code())
    print(email_code)
    user_email = email_code['email']
    response = post('http://web:8000/signup/email-confirm', json=email_code)
    assert response.status_code == 200
    assert response.json() == {"message": f"Email {user_email} successfully confirmed"}


user_test_data_email_confirm_user_not_found = {"email": "string", "code": 0}


def test_confirm_email_user_not_found():
    response = post('http://web:8000/signup/email-confirm', json=user_test_data_email_confirm_user_not_found)
    assert response.status_code == 200
    assert response.json() == {"error": "User not found"}
