# Dockerfile for generic Python projects with support for FastAPI
# Note: for the Anaconda stack and R support, please check out the data_science.Dockerfile

FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

EXPOSE 8080

RUN printf "Acquire::http::Pipeline-Depth 0;\nAcquire::http::No-Cache true;\nAcquire::BrokenProxy true;" > /etc/apt/apt.conf.d/99fixbadproxy

ENV BIND="0.0.0.0:8080"
ENV PORT=8080
ENV LOG_LEVEL=INFO

ENV DEBUG=0
ENV DEPLOYED=1

ENV WEB_CONCURRENCY=3

RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential

COPY requirements.txt ./

RUN pip install wheel
RUN pip install -r requirements.txt

COPY . /app
