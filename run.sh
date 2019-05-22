#!/bin/sh
. bin/activate
. .env

gunicorn main:app
