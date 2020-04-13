FROM library/python:3.8.2-alpine
LABEL maintainer="Joan Font <joanfont@gmail.com>"

WORKDIR /code

ADD requirements.txt .
RUN apk add --upgrade --no-cache --virtual .build-deps gcc libc-dev make \
    && pip3 install -r requirements.txt \
    && apk del .build-deps

ADD . /code/

ENTRYPOINT ["uvicorn", "app:app", "--host", "0.0.0.0"]