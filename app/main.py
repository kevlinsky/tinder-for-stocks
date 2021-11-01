import json
import logging
import datetime
from random import sample
from typing import List
from fastapi import FastAPI, Security, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from .worker import confirmation_email, password_reset
from user.schemas import (AuthModel, SignUpModel, RefreshTokenModel, PasswordResetRequestModel,
                          PasswordResetModel, UserScreenerModel)
from user.auth import Auth
from .db import User, UserCode, CodeTargetEnum
from screener.schemas import ScreenerModel, ShareScreenerModel
from screener.models import Screener
from screener.filter import filter_stocks
from stock.schemas import StockModel
from user.models import UserScreener

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
        hash = auth_handler.encode_confirm_token(user_details.email)
        confirmation_email.apply_async((user_details.email, hash))
        return {'id': id, 'message': 'Link for email verification was sent to specified email address'}
    except Exception as e:
        error_logger.error(e, exc_info=True)
        error_msg = 'Failed to signup user'
        return {'error': error_msg}


@app.get('/email-confirm/{hash}')
async def email_confirm(hash: str):
    user_email = auth_handler.decode_confirm_token(hash)
    user = await User.get_by_email(user_email)
    await User.update(user.id, is_active=True)
    return {'message': f'Email {user_email} successfully confirmed'}


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


@app.post('/user/{user_id}/screener')
async def create_screener(screener_details: ScreenerModel, user_id: int):
    user = await User.get(user_id)
    if user is None:
        return HTTPException(status_code=401, detail='User not found')
    if user.is_active:
        screener_id = await Screener.create(owner_id=user_id,
                                            public=screener_details.public,
                                            currency=screener_details.currency,
                                            market_sector=screener_details.market_sector,
                                            region=screener_details.region,
                                            index=screener_details.index,
                                            market_cap=screener_details.market_cap,
                                            ebitda=screener_details.ebitda,
                                            debt_equity=screener_details.debt_equity,
                                            p_e=screener_details.p_e,
                                            roa=screener_details.roa,
                                            roe=screener_details.roe,
                                            beta=screener_details.beta,
                                            revenue=screener_details.revenue,
                                            debt=screener_details.debt,
                                            expenses=screener_details.expenses,
                                            price=screener_details.price)
        await UserScreener.create(user_id=user_id, screener_id=screener_id)
        return {'id': screener_id, "message": "screener was successfully created"}
    else:
        error_msg = 'Verify your email'
        return {'error': error_msg}


@app.get('/user/{user_id}/screener', response_model=List[UserScreenerModel])
async def get_user_screeners(user_id: int):
    screeners = await UserScreener.get_users_screeners(user_id)
    return screeners


@app.get('/user/{user_id}/screener/{screener_id}', response_model=List[StockModel])
async def run_screener(screener_id: int, user_id: int):
    screener = await Screener.get(screener_id)
    if (screener.owner_id == user_id) | screener.public:
        result = await filter_stocks(screener)
        return result


@app.put('/user/{user_id}/screener/{screener_id}')
async def update_screener(screener_id: int, user_id: int, screener_details: ScreenerModel):
    screener = await Screener.get(id=screener_id)
    if screener.owner_id == user_id:
        await Screener.update(screener_id,
                              owner_id=user_id,
                              public=screener_details.public,
                              currency=screener_details.currency,
                              market_sector=screener_details.market_sector,
                              region=screener_details.region,
                              index=screener_details.index,
                              market_cap=screener_details.market_cap,
                              ebitda=screener_details.ebitda,
                              debt_equity=screener_details.debt_equity,
                              p_e=screener_details.p_e,
                              roa=screener_details.roa,
                              roe=screener_details.roe,
                              beta=screener_details.beta,
                              revenue=screener_details.revenue,
                              debt=screener_details.debt,
                              expenses=screener_details.expenses,
                              price=screener_details.price
                              )
        return {'message': f"screener {screener_id} was successfully updated"}
    else:
        error_msg = 'Sorry, you can update only your own screeners'
        return {'error': error_msg}


@app.delete('/user/{user_id}/screener/{screener_id}')
async def delete_screener(screener_id: int, user_id: int):
    screener = await Screener.get(id=screener_id)
    if screener.owner_id == user_id:
        await Screener.delete(screener_id)
        return {'message': f'Screener {screener_id} was successfully deleted'}
    else:
        error_msg = 'Sorry, you can delete only your own screeners'
        return {'error': error_msg}


@app.patch('/user/{user_id}/screener/{screener_id}')
async def share_screener(screener_id: int, user_id: int, screener_share: ShareScreenerModel):
    screener = await Screener.get(id=screener_id)
    if screener.owner_id == user_id:
        await Screener.update(screener_id,
                              public=screener_share.public)
        if screener.public:
            return {'message': f'Screener {screener_id} can be used by others now'}
        else:
            return {'message': f'Screener {screener_id} can not be used by others now'}
    else:
        error_msg = 'Sorry, you can share only your own screeners'
        return {'error': error_msg}
