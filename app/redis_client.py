import redis
import secrets
import os

client = redis.StrictRedis(
    host=os.environ.get('REDIS_HOST'),
    port=os.environ.get('REDIS_PORT'),
    db=2,
    charset="utf-8",
    decode_responses=True
)


def set_hash(email: str):
    hash = secrets.token_urlsafe(16)
    client.set(hash, email)
    return hash


def get_email(hash: str):
    email = client.get(hash)
    client.delete(hash)
    return email
