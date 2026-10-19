FROM python:3.14-alpine
WORKDIR /musichub
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY app ./app
CMD ["ls"]
