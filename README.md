# Tinder for stocks

## Common preparations
1. Create the logs dir and log files locally:
```
mkdir logs && cd logs && touch access_uvicorn.log error_uvicorn.log celery.log access_api.log error_api.log 
```

### How to launch with Docker?
1. Rename the ```.env.example``` file to ```.env```
```
cp .env.example .env
```
2. Run it with command:
```
docker-compose up --scale web=3
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

3. Make migrations:
```
alembic revision --autogenerate -m "Migration"
alembic upgrade head
```

4. Start message broker
```
redis-server
```

5. Run Celery worker and Celery beat
```
celery -A app.worker beat & \
celery -A app.worker.celery worker -l INFO --without-gossip --without-mingle --without-heartbeat -Ofair --pool=solo
```

6. Run FastAPI
```
uvicorn app.main:app
```

7. Open the **http://127.0.0.1:8000**


