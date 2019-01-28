FROM python:3.6-alpine

RUN apk update && \
  apk add --update \
    git \
    openssh-client \
    curl && \
    rm -rf /var/cache/apk/*

RUN pip3 install --upgrade pip

RUN adduser -h /backup -D backup

ENV PATH="/:${PATH}"

COPY python/* /

RUN pip3 install -r /requirements.txt

USER backup

ENTRYPOINT ["python3","/main.py"]