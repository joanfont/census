FROM library/python:3.8.2-alpine
LABEL maintainer="Joan Font <joanfont@gmail.com>"

ARG BUILD_ENV=prod

WORKDIR /code

ADD requirements*.txt ./
RUN apk add --upgrade --no-cache --virtual .build-deps gcc libc-dev make \
    && pip3 install -r requirements.txt \
    && test -e requirements-${BUILD_ENV}.txt && pip3 install -r requirements-${BUILD_ENV}.txt \
    && apk del .build-deps

ADD . /code/

ENV PYTHONPATH "/code:${PYTHONPATH}"
ENTRYPOINT ["uvicorn", "app:app", "--host", "0.0.0.0"]