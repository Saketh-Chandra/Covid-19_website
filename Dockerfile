FROM python:3.8

MAINTAINER SakethChandra "https://github.com/Saketh-Chandra/"

RUN apt-get -y install git
# RUN apt-get install python3 -y
# RUN apt install python3-pip -y

RUN git clone https://github.com/Saketh-Chandra/Covid-19_website.git

WORKDIR /Covid-19_website/

RUN pip3 install --trusted-host pypi.python.org --requirement requirements.txt

# ENTRYPOINT Flask_APP=/Covid-19_website/app.py flask run --host=0.0.0.0
CMD gunicorn --bind 0.0.0.0:5000 app:app
