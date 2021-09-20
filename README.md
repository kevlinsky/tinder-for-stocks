# tinder-for-stocks

## Launching
`uvicorn app.main:app --reload`

## Migrations
1. Generate: `alembic revision --autogenerate -m "Migration"`
2. Migrate: `alembic upgrade head`
