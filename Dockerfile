FROM library/python:3.7.2-alpine
LABEL maintainer "Joan Font <joanfont@gmail.com>"

WORKDIR /code

ADD requirements.txt .
RUN pip3 install -r requirements.txt

ADD . /code/

ENTRYPOINT ["gunicorn"]
CMD ["app:app", "-b", "0.0.0.0:8080"]