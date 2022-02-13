FROM python:3.8.12-slim-buster AS base
FROM base AS builder

RUN apt-get -qy update && apt-get install --no-install-recommends -y git libev-dev

RUN --mount=type=secret,id=GIT_ACCESS_TOKEN echo $(cat /run/secrets/GIT_ACCESS_TOKEN)
RUN --mount=type=secret,id=GIT_ACCESS_TOKEN git config --global url."https://$(cat /run/secrets/GIT_ACCESS_TOKEN)@github.com/".insteadOf "https://github.com/"

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN pip install --user pip -U
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

FROM base AS runtime

COPY --from=builder ${PYTHONPATH} ${PYTHONPATH}
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

COPY api /app/api

WORKDIR /app

EXPOSE 8000:8000

CMD ["python", "-m" ,"uvicorn", "api.main:app", "--host", "0.0.0.0"]
