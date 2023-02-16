FROM library/python:3.8-alpine3.17
RUN apk update && apk upgrade && apk add --no-cache make g++ bash git openssh postgresql-dev libffi-dev curl
RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
ADD . /usr/src/app
COPY ./django_project/ /usr/src/app
RUN pip install -r requirements.txt
EXPOSE 5000
CMD ["/bin/sh", "/home/user/launch.sh"]
