from pydantic import BaseModel, validator
from pydantic.networks import validate_email


class AuthModel(BaseModel):
    email: str
    password: str


class SignUpModel(BaseModel):
    email: str
    password: str
    first_name: str
    last_name: str

    @validator('email')
    def check_email(cls, value):
        (name, email) = validate_email(value)
        return email

    @validator('password')
    def check_password(cls, value):
        if 5 < len(value) < 21:
            return value
        else:
            raise ValueError('Password length must be between 6 and 20 characters')


class RefreshTokenModel(BaseModel):
    refresh_token: str


class PasswordResetRequestModel(BaseModel):
    email: str


class PasswordResetModel(BaseModel):
    email: str
    code: int
    new_password: str

    @validator('new_password')
    def check_new_password(cls, value):
        if 5 < len(value) < 21:
            return value
        else:
            raise ValueError('Password length must be between 6 and 20 characters')


class UserScreenerModel(BaseModel):
    screener_id: int
    user_id: int

    class Config:
        orm_mode = True
