#!/bin/sh
cd "$(dirname "$0")"

. bin/activate
. ./.env

pip install -r requirements.txt
exec gunicorn main:app --log-file=-
