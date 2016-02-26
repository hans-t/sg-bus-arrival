#!/bin/bash

ROOT=~/sites/$SITENAME
SOCKFILE=/tmp/$SITENAME.sock
MODULE_DIR=$ROOT/source/app/

NUM_WORKERS=3

cd $ROOT
source venv/bin/activate

exec gunicorn \
     --worker-class sync \
     --workers $NUM_WORKERS \
     --bind unix:$SOCKFILE \
     --chdir $MODULE_DIR \
     --log-level debug \
     --access-logfile $ROOT/logs/gunicorn-$SITENAME-access.log \
     --error-logfile $ROOT/logs/gunicorn-$SITENAME-error.log \
     app:app