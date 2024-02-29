FROM python:3.10-slim

SHELL ["/bin/bash", "-o", "pipefail", "-c"]

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1
ENV TZ=Europe/Madrid
ENV DEBIAN_FRONTEND noninteractive

# hadolint ignore=DL3059,DL3008
RUN apt-get update && \
    apt-get -y upgrade && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# hadolint ignore=DL3059
RUN addgroup lift && adduser lift --ingroup lift --home /opt/lift && chown -R lift:lift /opt/lift
ENV PATH=/opt/lift/.local/bin:$PATH

# hadolint ignore=DL3059
RUN pip3 install --no-cache-dir poetry==1.4

WORKDIR /opt/lift/src

RUN poetry config virtualenvs.create false
COPY pyproject.toml poetry.lock ./
RUN poetry install

ENV PYTHONPATH /opt/lift/src
COPY --chown=lift . .

USER lift

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--threads", "4", "--log-level", "warning", "src.delivery.api.main:create_app()"]

