FROM python:3.8.12-slim-buster AS base
FROM base AS builder

ENV RESEARCH_DATA_WHEEL=research_data-0.0.3-py3-none-any.whl
ENV RESEARCH_WHEEL=research-0.0.4-py3-none-any.whl
ENV RESEARCH_MOGA_WHEEL=research_moga-0.0.2-py3-none-any.whl

COPY pyproject.toml pyproject.toml
COPY ${RESEARCH_DATA_WHEEL} ${RESEARCH_DATA_WHEEL}
COPY ${RESEARCH_WHEEL} ${RESEARCH_WHEEL}
COPY ${RESEARCH_MOGA_WHEEL} ${RESEARCH_MOGA_WHEEL}

ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

FROM base AS runtime

COPY --from=builder ${PYTHONPATH} ${PYTHONPATH}
ENV PYTHONPATH=${PYTHONPATH}:${PWD}

COPY .env.production .env
COPY moga_tracking /app/moga_tracking
COPY ./.aws/credentials /root/.aws/credentials
COPY ./research-data.sqlite /app/research-data.sqlite

WORKDIR /app
EXPOSE 3000:3000

CMD ["python", "-m" ,"uvicorn", "moga_tracking.__main__:app", "--host", "0.0.0.0", "--port", "3000"]