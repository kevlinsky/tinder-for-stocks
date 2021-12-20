import random
import string


def random_char(char_num):
    return ''.join(random.choice(string.ascii_letters) for _ in range(char_num))


server_path = 'http://web:8080'

signup_user_test_data = {'email': random_char(7) + "@gmail.com", 'password': 'tinder', 'first_name': 'tinder',
                         'last_name': 'tinder'}

signup_user_test_invalid_data = {'email': random_char(6), 'password': 'tinder', 'first_name': 'tinder',
                                 'last_name': 'tinder'}

confirm_user_test_data = {'email': random_char(8) + "@gmail.com", 'password': 'tinder', 'first_name': 'tinder',
                          'last_name': 'tinder'}

login_user_test_data_not_verified = {'email': random_char(5) + "@gmail.com", 'password': 'tinder',
                                     'first_name': 'tinder', 'last_name': 'tinder'}

login_user_test_data = {'email': random_char(9) + "@gmail.com", 'password': 'tinder',
                        'first_name': 'tinder', 'last_name': 'tinder'}

password_reset_user_test_data = {'email': random_char(4) + "@gmail.com", 'password': 'tinder',
                                 'first_name': 'tinder', 'last_name': 'tinder'}
test_user_screener_data = {'email': random_char(10) + "@gmail.com", 'password': 'tinder', 'first_name': 'tinder',
                           'last_name': 'tinder'}
test_screener_data = {
    "public": False,
    "currency": "USD",
    "market_sector": "REAL ESTATE & CONSTRUCTION",
    "region": "USA",
    "exchange": "NYSE",
    "market_cap": "7758675999 - 7758676001",
    "ebitda": "392999999 - 393000001",
    "debt_equity": "268 - 270",
    "p_e": "68 - 70",
    "roa": "0 - 1",
    "roe": "0 - 1",
    "beta": "1 - 2",
    "revenue": "4 - 5",
    "debt": "92 - 95",
    "price": ""
}
