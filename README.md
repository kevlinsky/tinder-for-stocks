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

2. Run migrations:
```
alembic upgrate head
```

3. Run FastAPI
```
uvicorn app.main:app
```
4. Open the **http://127.0.0.1:8000**