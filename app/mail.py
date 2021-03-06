from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
import os
from jinja2 import Environment, PackageLoader, select_autoescape
from stock.recommender import Recommender

env = Environment(
    loader=PackageLoader('app', 'email_templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

conf = ConnectionConfig(
    MAIL_USERNAME=os.environ.get('MAIL_USERNAME'),
    MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD'),
    MAIL_FROM='stocks.tinder2021@gmail.com',
    MAIL_PORT=587,
    MAIL_SERVER='smtp.gmail.com',
    MAIL_FROM_NAME='Tinder For Stocks Helper',
    MAIL_TLS=True,
    MAIL_SSL=False,
    USE_CREDENTIALS=True,
    VALIDATE_CERTS=False
)


async def send_confirmation_email(email_to: str, hash: str):
    template = env.get_template('confirm_email.html')

    message = MessageSchema(
        subject='Email Confirmation',
        recipients=[email_to],
        html=template.render(hash=hash),
        subtype='html',
    )

    fm = FastMail(conf)
    await fm.send_message(message)


async def send_password_reset_email(email_to: str, code: int):
    template = env.get_template('password_reset.html')

    message = MessageSchema(
        subject='Password Reset',
        recipients=[email_to],
        html=template.render(code=code),
        subtype='html',
    )

    fm = FastMail(conf)
    await fm.send_message(message)


async def send_weekly_digest():
    digest = await Recommender().generate_weekly_digest()
    fm = FastMail(conf)
    template = env.get_template('weekly_digest.html')

    for pair in digest:
        message = MessageSchema(
            subject='Weekly digest',
            recipients=[pair['user'].email],
            html=template.render(first_name=pair['user'].first_name, stocks=pair['stocks']),
            subtype='html',
        )

        await fm.send_message(message)


async def send_monthly_digest():
    digest = await Recommender().generate_monthly_digest()
    fm = FastMail(conf)
    template = env.get_template('monthly_digest.html')

    for pair in digest:
        message = MessageSchema(
            subject='Monthly digest',
            recipients=[pair['user'].email],
            html=template.render(first_name=pair['user'].first_name, stocks=pair['stocks']),
            subtype='html',
        )

        await fm.send_message(message)
