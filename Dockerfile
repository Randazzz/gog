FROM python:3.12

RUN apt-get update && apt-get install -y netcat-openbsd && apt-get clean

RUN mkdir -p /gogserver/gog

WORKDIR /gogserver/gog

COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY . .

RUN mkdir -p /gogserver/gog/staticfiles
RUN mkdir -p /gogserver/gog/media

WORKDIR /gogserver/gog
