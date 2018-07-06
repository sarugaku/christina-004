FROM ubuntu:18.04

# -- Install Pipenv:
RUN apt update && apt install python3-pip git -y && pip3 install pipenv

ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8
ENV FUTURE_GADGET_LAB pypa/pipenv
ENV USERNAME christina-004
ENV GITHUB_TOKEN
ENV GITHUB_SECRET
ENV PORT 8000

RUN set -ex && mkdir /app

WORKDIR /app


COPY . /app

RUN set -ex && pipenv install --deploy --system

CMD python -m christina