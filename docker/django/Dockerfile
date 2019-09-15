FROM ubuntu:latest


RUN mkdir -p /data/django
WORKDIR /data/django

ADD ./requirements.txt /data/django

RUN apt-get update && apt-get install -y
RUN apt-get install python3-pip \
                    python3-dev \
		            libpq-dev \
		            npm \
                    -y

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt