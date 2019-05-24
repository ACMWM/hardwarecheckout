#!/bin/sh
cd "$(dirname "$0")"

. bin/activate
. ./.env

exec gunicorn main:app --log-file=- --access-logfile=- --capture-output
