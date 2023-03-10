FROM library/python:3.8-alpine3.17
RUN apk update && apk upgrade && apk add --no-cache make g++ bash git openssh postgresql-dev libffi-dev curl
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
ADD ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt
COPY . /usr/src/app
RUN python3 setup.py install
EXPOSE 5000
CMD ["/bin/sh", "./launch.sh"]
