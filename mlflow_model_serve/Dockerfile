FROM python:3.8.12-slim-buster AS base
FROM base AS builder

ENV RESEARCH_WHEEL=research-0.0.3-py3-none-any.whl

COPY requirements.txt requirements.txt
COPY ${RESEARCH_WHEEL} ${RESEARCH_WHEEL}

RUN pip install --user pip -U
RUN pip install --user -r requirements.txt
RUN pip install --user ${RESEARCH_WHEEL}

FROM base AS runtime

COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

COPY .env .env
COPY api /app/api
COPY .aws/credentials /root/.aws/credentials

WORKDIR /app

EXPOSE 8000:8000

CMD ["python", "-m" ,"uvicorn", "api.main:app", "--host", "0.0.0.0"]