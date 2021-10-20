import os
import asyncio
import logging

from celery import Celery
from celery.utils.log import get_task_logger

from .mail import send_confirmation_email, send_password_reset_email

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

celery = Celery(__name__)
celery.conf.broker_url = os.environ.get('CELERY_BROKER_URL')
celery.conf.result_backend = os.environ.get('CELERY_RESULT_BACKEND')

logger = get_task_logger(__name__)
logger_handler = logging.FileHandler(os.path.join(BASE_DIR, 'logs/celery.log'))
logger_handler.setFormatter(
    logging.Formatter("%(levelname)s: [%(asctime)s] - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"))
logger.addHandler(logger_handler)


@celery.task(name='confirmation_email')
def confirmation_email(email_to: str, hash: str):
    asyncio.get_event_loop().run_until_complete(send_confirmation_email(email_to, hash))
    logger.info(f"confirmation email to {email_to} has been sent")
    return {'message': f'Confirmation email to {email_to} has been sent'}


@celery.task(name='password_reset')
def password_reset(email_to: str, code: int):
    asyncio.get_event_loop().run_until_complete(send_password_reset_email(email_to, code))
    logger.info(f"password reset to {email_to} has been sent")
    return {'message': f'Password reset email to {email_to} has been sent'}
