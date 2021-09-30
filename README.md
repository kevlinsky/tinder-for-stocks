# Tinder for stocks

### How to launch with Docker?
1. Rename the ```.env.example``` file to ```.env```
```
cp .env.example .env
```
2. Run it with command:
```
docker-compose up
```
3. Open the **http://0.0.0.0:8000**

### How to launch without Docker?
1. Environment variables:
* Add the environment variables in ```File/Settings/Tools/Terminal``` if you're using PyCharm
* **Or** add it in ```~/.bashrc```

2. Install dependencies (if you doesn't have pipenv, install it: ```pip install pipenv```):
```
pipenv shell
pipenv install 
```

3. Migrations:
```
alembic revision --autogenerate -m "Migration"
alembic upgrade head
```

4. Run FastAPI
```
uvicorn app.main:app
```

5. Message Broker
```
redis-server
```

6. Celery
```
celery -A app.worker.celery worker -l INFO --without-gossip --without-mingle --without-heartbeat -Ofair --pool=solo
```

7. Open the **http://127.0.0.1:8000**


