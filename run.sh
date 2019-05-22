#!/bin/sh
. bin/activate
. ./.env

pip install -r requirements.txt
gunicorn main:app --log-file=-
