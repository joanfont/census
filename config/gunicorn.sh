#!/bin/bash

export WORKON_HOME=~/.virtualenvs/
source /usr/local/bin/virtualenvwrapper.sh
workon electoral-census

PROJECT_DIR=/opt/electoral-census/

USER=root
GROUP=root
LOGFILE=${PROJECT_DIR}/log/gunicorn.log
LOGERRFILE=${PROJECT_DIR}/log/gunicorn_err.log

LOGDIR=$(dirname $LOGFILE)

NUM_WORKERS=3
TIMEOUT=60

cd ${PROJECT_DIR}
export PYTHONPATH=${PROJECT_DIR}:${PYTHONPATH}

test -d ${LOGDIR} || mkdir -p ${LOGDIR}

exec gunicorn app:app -w ${NUM_WORKERS} -b 127.0.0.1:8080\
    --user=${USER} --group=${GROUP}\
    --log-level=info --log-file=${LOGFILE} 2>> ${LOGERRFILE}