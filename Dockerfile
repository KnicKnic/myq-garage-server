
# Pull base image
FROM ubuntu

# Install dependencies
RUN apt-get update --fix-missing \
 && apt-get install -y \
    python3 \
    python3-dev \
    python3-pip \
    python3-virtualenv \
    python3-flask \
    python3-requests \
    --no-install-recommends \
 && rm -rf /var/lib/apt/lists/*

COPY /flask_prog.py /data/
COPY /myq-garage/myq-garage.py /data/
COPY /myq-garage/config.ini /data/
# Define working directory
WORKDIR /data

# Define default command
CMD ["python3", "flask_prog.py"]
