#!/bin/sh
cd "$(dirname "$0")"

. bin/activate
. ./.env

pip install -r requirements.txt
gunicorn main:app --log-file=-
