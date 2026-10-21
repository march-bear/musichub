FROM python:3.14-slim
WORKDIR /musichub

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY migrations ./migrations
COPY alembic.ini .
COPY app/data/models.py ./app/data/
