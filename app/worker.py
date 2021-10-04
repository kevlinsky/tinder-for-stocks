import os
import asyncio
from celery import Celery

from .mail import send_confirmation_email, send_password_reset_email

celery = Celery(__name__)
celery.conf.broker_url = 'redis://' + os.environ.get('CELERY_BROKER_HOST') + ':' + os.environ.get(
    'CELERY_BROKER_PORT') + '/0'
celery.conf.result_backend = 'redis://' + os.environ.get('CELERY_BROKER_HOST') + ':' + os.environ.get(
    'CELERY_BROKER_PORT') + '/1'


@celery.task(name='confirmation_email')
def confirmation_email(email_to: str, hash: str):
    asyncio.get_event_loop().run_until_complete(send_confirmation_email(email_to, hash))
    return {'message': f'Confirmation email to {email_to} has been sent'}


@celery.task(name='password_reset')
def password_reset(email_to: str, code: int):
    asyncio.get_event_loop().run_until_complete(send_password_reset_email(email_to, code))
    return {'message': f'Password reset email to {email_to} has been sent'}
