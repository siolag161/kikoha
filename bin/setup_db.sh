#!/usr/bin/env bash

#echo DJANGO_SETTINGS_MODULE=config.settings.dev >> .env.dev
#echo PYTHONPATH={{ project_name }} >> .env.dev
#echo PYTHONUNBUFFERED=True >> .env.dev
#echo PYTHONWARNINGS=ignore:RemovedInDjango18Warning >> .env.dev
#echo CACHE=dummy >> .env.dev

#echo "env: .env.dev" > .foreman
#echo "procfile: Procfile.dev" >> .foreman

#workon {{ project_name }}-dev
#createdb {{ project_name }}-dev
#foreman run django-admin.py migrate
