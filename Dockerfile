FROM ubuntu:20.04

# Create limited user for Celery
RUN groupadd user && useradd --create-home --home-dir /home/user -g user user

# Set WORKDIR to /home/user
WORKDIR /home/user

ADD . /home/user

# Update packages and install pip
RUN DEBIAN_FRONTEND=noninteractive apt-get update -y && \
    apt -y dist-upgrade && \
    apt-get -y --no-install-recommends install python3 python3-pip python3-dev libpq-dev libffi-dev gcc curl && \
    pip3 install -r requirements.txt && \
    python3 setup.py install && \
    apt -y remove gcc python3-pip && \
    apt -y clean && \
    rm -rf /var/lib/apt/lists/*

# Expose
EXPOSE 5000

# Set user
USER user
