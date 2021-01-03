# Dockerfile copied from - https://github.com/michael0liver/python-poetry-docker-example/blob/master/docker/Dockerfile

# Uses multi-stage builds requiring Docker 17.05 or higher
# See https://docs.docker.com/develop/develop-images/multistage-build/

# Creating a python base with shared environment variables
FROM python:slim@sha256:4d92968b26bb6b7b62d957244de86fc1054f03793577d49e85c00864eb03ca07 as python-base
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    POETRY_NO_INTERACTION=1 \
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"


# builder-base is used to build dependencies
FROM python-base as builder-base
RUN apt-get update \
    && apt-get install --no-install-recommends -y \
        curl \
        build-essential

RUN apt-get install  --no-install-recommends -y \
        libffi-dev \
        gcc 

# Install Poetry - respects $POETRY_VERSION & $POETRY_HOME
ENV POETRY_VERSION=1.1.4

# 1.1.4 commit sha for install
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/8312e3f2dbfa126cd311c666fea30656941e1bd3/get-poetry.py | python

# We copy our Python requirements here to cache them
# and install only runtime deps using poetry
WORKDIR $PYSETUP_PATH
COPY ./poetry.lock ./pyproject.toml ./
RUN poetry install --no-dev  # respects 



# 'production' stage uses the clean 'python-base' stage and copyies
# in only our runtime deps that were installed in the 'builder-base'
FROM python-base as production
ENV FASTAPI_ENV=production

# since we had to install libffi-dev when building
#    install libffi6 when running
RUN apt-get install  --no-install-recommends -y \
        libffi6 \
    \
	&& apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
	&& rm -rf /var/lib/apt/lists/*


COPY --from=builder-base $VENV_PATH $VENV_PATH

COPY *.py /app/
WORKDIR /app

EXPOSE "80"

# Define default command
CMD ["python3", "flask_prog.py"]