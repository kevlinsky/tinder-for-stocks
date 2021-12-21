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
