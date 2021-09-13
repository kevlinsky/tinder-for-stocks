from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

import os

host = os.environ.get('DB_HOST')
name = os.environ.get('DB_NAME')
port = os.environ.get('DB_PORT')
user = os.environ.get('DB_USER')
password = os.environ.get('DB_USER_PASSWORD')

SQLALCHEMY_DATABASE_URL = f'postgresql://{user}:{password}@{host}:{port}/{name}'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception:
        db.close()
