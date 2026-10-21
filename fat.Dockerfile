FROM python:3.14-slim
WORKDIR /musichub

RUN apt-get update && apt-get install -y --no-install-recommends \
        fluidsynth \
        fluid-soundfont-gm \
        ffmpeg \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
COPY worker-requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN pip install -r worker-requirements.txt

COPY app ./app
COPY alembic.ini .
COPY migrations ./migrations
