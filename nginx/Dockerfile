FROM nginx:latest
FROM python:3.9
COPY nginx.conf /etc/nginx/nginx.conf

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/usr/src/

CMD python wait-postgres.py && \
    alembic upgrade head && \
    python app/init_stocks.py &&\
    uvicorn app.main:app --host 0.0.0.0 --port 8000