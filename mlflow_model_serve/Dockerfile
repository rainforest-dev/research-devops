FROM python:3.8.12-slim-buster AS base
FROM base AS builder

COPY pyproject.toml pyproject.toml

ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN pip install --user pip -U
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

FROM base AS runtime

COPY --from=builder ${PYTHONPATH} ${PYTHONPATH}
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

COPY .env .env
COPY api /app/api
COPY ./.aws/credentials /root/.aws/credentials

WORKDIR /app

EXPOSE 8000:8000

CMD ["python", "-m" ,"uvicorn", "api.main:app", "--host", "0.0.0.0"]