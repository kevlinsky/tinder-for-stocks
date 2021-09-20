from fastapi import FastAPI, Security, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from user.schemas import AuthModel, SignUpModel, RefreshTokenModel
from user.auth import Auth
from .db import User

app = FastAPI()
security = HTTPBearer()
auth_handler = Auth()


@app.get('/')
async def index():
    return {'hello': 'world'}


@app.post('/signup')
async def signup(user_details: SignUpModel):
    result_user = await User.get_by_email(user_details.email)
    if result_user is not None:
        return 'Account already exists'
    try:
        hashed_password = auth_handler.encode_password(user_details.password)
        id = await User.create(email=user_details.email,
                               password=hashed_password,
                               first_name=user_details.first_name,
                               last_name=user_details.last_name)
        return {'id': id, 'message': 'Verification code was sent to the specified email'}
    except Exception:
        error_msg = 'Failed to signup user'
        return {'error': error_msg}


@app.post('/token')
async def login(user_details: AuthModel):
    user = await User.get_by_email(user_details.email)
    if user is None:
        return HTTPException(status_code=401, detail='Invalid email')
    if not auth_handler.verify_password(user_details.password, user.password):
        return HTTPException(status_code=401, detail='Invalid password')
    if user.is_active:
        access_token = auth_handler.encode_token(user.email)
        refresh_token = auth_handler.encode_refresh_token(user.email)
        return {'access_token': access_token, 'refresh_token': refresh_token}
    else:
        return {'error': 'Verify your email'}


@app.post('/token/refresh')
async def refresh_token(refresh_model: RefreshTokenModel):
    refresh_token = refresh_model.refresh_token
    new_token = auth_handler.refresh_token(refresh_token)
    return {'access_token': new_token}


@app.post('/secret')
async def secret_data(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    if auth_handler.decode_token(token):
        return {'message': 'Top Secret data. Only authorized users can access this info'}


@app.get('/notsecret')
async def not_secret_data():
    return {'message': 'Not secret data'}
