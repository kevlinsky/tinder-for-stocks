import logging
import datetime
from random import sample

from fastapi import FastAPI, Security, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .worker import confirmation_email, password_reset
from user.schemas import (AuthModel, SignUpModel, RefreshTokenModel, PasswordResetRequestModel, EmailConfirmationModel,
                          PasswordResetModel)
from user.auth import Auth
from .db import User, UserCode, CodeTargetEnum

app = FastAPI()
security = HTTPBearer()
auth_handler = Auth()

access_logger = logging.getLogger('uvicorn.access')
error_logger = logging.getLogger('uvicorn.error')
access_handler = logging.FileHandler(filename='./logs/access_uvicorn.log', mode='a')
error_handler = logging.FileHandler(filename='./logs/error_uvicorn.log', mode='a')


@app.on_event('startup')
async def startup_event():
    error_logger.setLevel('WARNING')

    access_handler.setFormatter(
        logging.Formatter("%(levelname)s: [%(asctime)s] - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
    error_handler.setFormatter(
        logging.Formatter("%(levelname)s: [%(asctime)s] - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))

    access_logger.addHandler(access_handler)
    error_logger.addHandler(error_handler)


@app.on_event('shutdown')
async def shutdown_event():
    access_handler.close()
    error_handler.close()


@app.get('/')
async def index():
    return {'hello': 'world'}


def generate_code():
    digits = sample(range(1, 10), 5)
    str_digits = [str(digit) for digit in digits]
    return int(''.join(str_digits))


@app.post('/signup')
async def signup(user_details: SignUpModel):
    result_user = await User.get_by_email(user_details.email)
    if result_user is not None:
        error_msg = 'Account already exists'
        return {'error': error_msg}
    try:
        hashed_password = auth_handler.encode_password(user_details.password)
        id = await User.create(email=user_details.email,
                               password=hashed_password,
                               first_name=user_details.first_name,
                               last_name=user_details.last_name)
        confirmation_code = generate_code()
        confirmation_email.apply_async((user_details.email, confirmation_code))
        await UserCode.create(user_id=id,
                              code=confirmation_code,
                              target=CodeTargetEnum.EMAIL_VERIFICATION)
        return {'id': id, 'message': 'Verification code was sent to the specified email'}
    except Exception as e:
        error_logger.error(e, exc_info=True)
        error_msg = 'Failed to signup user'
        return {'error': error_msg}


@app.post('/signup/email-confirm')
async def signup_email_confirm(details: EmailConfirmationModel):
    user = await User.get_by_email(details.email)
    if user is None:
        error_msg = 'User not found'
        return {'error': error_msg}
    else:
        user_code = await UserCode.get_by_user_and_target(user.id, CodeTargetEnum.EMAIL_VERIFICATION)
        if user_code.code != details.code:
            error_msg = 'Wrong code for specified user'
            return {'error': error_msg}
        else:
            await User.update(user.id, is_active=True)
            await UserCode.delete(user_code.id)
            return {'message': f'Email {details.email} successfully confirmed'}


@app.post('/login')
async def login(user_details: AuthModel):
    user = await User.get_by_email(user_details.email)
    if user is None:
        return HTTPException(status_code=401, detail='User not found')
    if not auth_handler.verify_password(user_details.password, user.password):
        return HTTPException(status_code=401, detail='Invalid password')
    if user.is_active:
        access_token = auth_handler.encode_token(user.email)
        refresh_token = auth_handler.encode_refresh_token(user.email)
        return {'access_token': access_token, 'refresh_token': refresh_token}
    else:
        error_msg = 'Verify your email'
        return {'error': error_msg}


@app.post('/token/refresh')
async def refresh_token(refresh_model: RefreshTokenModel):
    refresh_token_ = refresh_model.refresh_token
    new_token = auth_handler.refresh_token(refresh_token_)
    return {'access_token': new_token}


@app.post('/password-reset/request')
async def request_password_reset(request_model: PasswordResetRequestModel):
    user = await User.get_by_email(request_model.email)
    if user is None:
        return HTTPException(status_code=401, detail='User not found')
    else:
        check_code = await UserCode.get_by_user_and_target(user.id, CodeTargetEnum.PASSWORD_RESET)
        if check_code is not None:
            if datetime.datetime.now().timestamp() - check_code.datetime.timestamp() > 60:
                await UserCode.delete(check_code.id)
                reset_code = generate_code()
                password_reset.apply_async((request_model.email, reset_code))
                await UserCode.create(user_id=user.id,
                                      code=reset_code,
                                      target=CodeTargetEnum.PASSWORD_RESET)
                return {'message': 'Reset code was sent on specified email'}
            else:
                return {'message': 'You can request a reset code only one time per minute'}
        reset_code = generate_code()
        password_reset.apply_async((request_model.email, reset_code))
        await UserCode.create(user_id=user.id,
                              code=reset_code,
                              target=CodeTargetEnum.PASSWORD_RESET)
        return {'message': 'Reset code was sent on specified email'}


@app.post('/password-reset')
async def password_reset_confirm(reset_model: PasswordResetModel):
    user = await User.get_by_email(reset_model.email)
    if user is None:
        return HTTPException(status_code=401, detail='User not found')
    else:
        code_model = await UserCode.get_by_user_and_target(user.id, CodeTargetEnum.PASSWORD_RESET)
        if code_model.code != reset_model.code:
            return HTTPException(status_code=401, detail='Wrong code for specified user')
        else:
            hashed_password = auth_handler.encode_password(reset_model.new_password)
            await User.update(user.id, password=hashed_password)
            await UserCode.delete(code_model.id)
            return {'message': 'Password was changed successfully'}


@app.post('/secret')
async def secret_data(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    if auth_handler.decode_token(token):
        return {'message': 'Top Secret data. Only authorized users can access this info'}


@app.get('/notsecret')
async def not_secret_data():
    return {'message': 'Not secret data'}
