FROM python:3.9

RUN apt-get install && apt update && apt install vim -y

ENV PYTHONUNBUFFERED=1
ENV PYTHONPATH=/usr/src/

WORKDIR /usr/src/
RUN pip install pipenv
COPY Pipfile Pipfile.lock ./
RUN pipenv install --ignore-pipfile --system --deploy

COPY . ./

CMD python wait-postgres.py && \
    pytest