FROM python:3.11-slim-buster

COPY ./migrations ./migrations
COPY ./database/models.py ./database/models.py
COPY ./alembic.ini .
COPY ./alembic_upgrade.sh .
WORKDIR .

RUN python3 -m pip install alembic psycopg2-binary asyncpg python-dotenv

RUN ["chmod", "+x", "./alembic_upgrade.sh"]
