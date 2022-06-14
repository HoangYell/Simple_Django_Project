#!/bin/sh
# git clone & activate virtual env
git clone git@github.com:ngohoangyell/Simple_Django_Project.git
cd Simple_Django_Project
python3 -m venv hybeta_env
source hybeta_env/bin/activate
# install python packages
python3 -m pip install -r requirements.txt
# install coding cleaner, helpful for coding, you can skip it
pre-commit install
pre-commit run --all-files
# create database model
python manage.py migrate
# run pytest
pytest -s
# start server
python manage.py runserver


#==========================Some more info if you have time===============================
# Create example data for list view
# sh create_example_data.sh

# Command to start django project from 0
# django-admin startproject hybeta .
# python manage.py startapp jobs
# PYTHONUNBUFFERED=1;DJANGO_SETTINGS_MODULE=hybeta.settings.test python manage.py shell

# Tips:
# kill port: kill -9 $(lsof -ti:8000)
