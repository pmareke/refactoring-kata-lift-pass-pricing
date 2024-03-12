FROM python:3.10-slim

RUN pip3 install --no-cache-dir poetry

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry install

COPY . .

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "src.delivery.api.main:create_app()"]

