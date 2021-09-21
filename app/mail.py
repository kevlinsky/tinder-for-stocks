from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
import os
from jinja2 import Environment, PackageLoader, select_autoescape

env = Environment(
    loader=PackageLoader('app', 'email_templates'),
    autoescape=select_autoescape(['html'])
)

conf = ConnectionConfig(
    MAIL_USERNAME=os.environ.get('MAIL_USERNAME'),
    MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD'),
    MAIL_FROM='tinder-for-stocks@gmail.com',
    MAIL_PORT=587,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_FROM_NAME='Tinder For Stocks Helper',
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=True
)


async def send_confirmation_email(email_to: str, code: int):
    template = env.get_template('confirm_email.html')

    message = MessageSchema(
        subject='Email Confirmation',
        recipients=[email_to],
        body=template.render(code=code),
        subtype='html',
    )

    fm = FastMail(conf)
    await fm.send_message(message)


async def send_password_reset_email(email_to: str, code: int):
    template = env.get_template('password_reset.html')

    message = MessageSchema(
        subject='Password Reset',
        recipients=[email_to],
        body=template.render(code=code),
        subtype='html',
    )

    fm = FastMail(conf)
    await fm.send_message(message)
