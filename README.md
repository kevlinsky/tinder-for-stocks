# tinder-for-stocks

## Launching
`uvicorn app.main:app --reload`

## Migrations
1. Generate: `alembic revision --autogenerate -m "Migration"`
2. Migrate: `alembic upgrade head`

## Message Broker
`redis-server`

## Worker
`celery -A app.worker.celery worker -l INFO --without-gossip --without-mingle --without-heartbeat -Ofair --pool=solo`