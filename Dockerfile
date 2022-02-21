FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive
ARG TZ=Europe/Moscow

WORKDIR /code

RUN apt update && apt install python3.8 python3-pip -y
RUN pip install --upgrade pip 
RUN apt install libpq-dev -y
RUN update-alternatives --install /usr/bin/pip pip /usr/bin/pip3 1

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN apt-get update && playwright install firefox && playwright install-deps 

COPY . /code/


