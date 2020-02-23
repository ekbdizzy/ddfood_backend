FROM python:3.7

RUN mkdir /project -p
WORKDIR /project
ADD requirements.txt /project
RUN pip3 install -r requirements.txt
ADD . /project