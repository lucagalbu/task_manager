FROM python:3.10.13-bookworm

COPY backend_entrypoint.sh /tools/entrypoint.sh
RUN chmod +x /tools/entrypoint.sh

RUN curl -sSL https://install.python-poetry.org | POETRY_VERSION=1.6.1 POETRY_HOME=/usr/local/ python3 -
