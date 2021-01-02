
# Pull base image
FROM debian:latest@sha256:5b5fa7e155b1f19dffb996ea64e55520b80d5bd7a8fdb5aed1acabd217e9ed59

# Install dependencies
RUN apt-get update --fix-missing \
 && apt-get install -y \
    python3 \
    python3-dev \
    python3-pip \
    python3-virtualenv \
    python3-flask \
    python3-requests \
    gcc \
    libffi-dev \
    python3-setuptools \
    --no-install-recommends 


#  && rm -rf /var/lib/apt/lists/*

RUN apt-get install libssl-dev  -y

RUN pip3 install --upgrade pip poetry
# RUN pip3 install --upgrade pip pymyq aiohttp flask

# Define working directory
WORKDIR /data
COPY * /data/



RUN poetry install

EXPOSE "80"

# Define default command
CMD ["python3", "flask_prog.py"]
