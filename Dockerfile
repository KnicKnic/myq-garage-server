
# Pull base image
FROM debian

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
    --no-install-recommends \
 && rm -rf /var/lib/apt/lists/*

RUN pip3 install --upgrade pip
RUN pip3 install pymyq
RUN pip3 install aiohttp
RUN pip3 install flask

COPY *.py /data/
# Define working directory
WORKDIR /data

# Define default command
CMD ["python3", "flask_prog.py"]
