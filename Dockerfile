FROM python:3.8

MAINTAINER SakethChandra "https://github.com/Saketh-Chandra/"

RUN apt-get update -y
RUN apt-get -y install git
RUN apt-get install python3 -y
RUN apt-get -y install python3-pip

RUN git clone https://github.com/Saketh-Chandra/Covid-19_website.git

WORKDIR /Covid-19_website/

RUN pip3 install --trusted-host pypi.python.org --requirement requirements.txt

ENV port=5000

# ENTRYPOINT Flask_APP=/Covid-19_website/app.py flask run --host=0.0.0.0
CMD gunicorn --bind 0.0.0.0:$port app:app
