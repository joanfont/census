#!/bin/bash
. /home/census/virtualenv/bin/activate

WSGI_APPLICATION=app:app
BIND_HOST=127.0.0.1
BIND_PORT=5000
PROJECT_DIR=/home/census/src
USER=census
GROUP=census
LOG_FILE=${PROJECT_DIR}/log/gunicorn.log
ERROR_LOG_FILE=${PROJECT_DIR}/log/gunicorn_err.log

LOGDIR=$(dirname ${LOG_FILE})

NUM_WORKERS=3
TIMEOUT=60

cd ${PROJECT_DIR}
export PYTHONPATH=${PROJECT_DIR}:${PYTHONPATH}

test -d ${LOGDIR} || mkdir -p ${LOGDIR}

exec gunicorn ${WSGI_APPLICATION} -w ${NUM_WORKERS} -b ${BIND_HOST}:${BIND_PORT}\
    --user=${USER} --group=${GROUP}\
    --log-level=info --log-file=${LOG_FILE} 2>> ${ERROR_LOG_FILE}
