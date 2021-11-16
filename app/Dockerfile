FROM python:3.9

RUN apt-get install && apt update && apt install vim -y

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/usr/src/
WORKDIR /usr/src/
RUN pip install pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install --ignore-pipfile --system --deploy

COPY . ./

CMD alembic upgrade head && \
    python app/init_stocks.py &&\
    celery -A app.worker beat & \
    celery -A app.worker.celery worker -l INFO --without-gossip --without-mingle --without-heartbeat -Ofair --pool=solo & \
    uvicorn app.main:app --host 0.0.0.0 --port 8000