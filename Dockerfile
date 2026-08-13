FROM python:3.13-slim-trixie AS build

RUN apt-get update \
    && apt-get install --no-install-suggests --no-install-recommends -y gcc libc6-dev \
    && ln -s /usr/local/bin/python /usr/bin/python \
    && /usr/bin/python -m venv /venv \
    && /venv/bin/pip install --upgrade pip setuptools wheel

COPY requirements.txt /requirements.txt

RUN /venv/bin/pip install --no-cache-dir -r /requirements.txt


FROM gcr.io/distroless/python3-debian13:nonroot
COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:1.0.1 /lambda-adapter /opt/extensions/lambda-adapter

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000
LABEL build.version="lambda-v4"

WORKDIR /app

COPY --from=build /venv /venv
COPY ml ./ml
COPY model ./model

EXPOSE 8000

ENTRYPOINT ["/venv/bin/python3", "-m", "uvicorn", "ml.api:app", "--host", "0.0.0.0", "--port", "8000"]
