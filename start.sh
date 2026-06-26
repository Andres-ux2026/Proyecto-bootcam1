#!/usr/bin/env bash
set -o errexit

export DJANGO_SETTINGS_MODULE=akelagym.settings

exec gunicorn akelagym.wsgi --bind 0.0.0.0:$PORT
