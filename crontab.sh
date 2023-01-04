#!/bin/bash 

source env/bin/activate ; ./manage.py crawlcomics ; sudo systemctl daemon-reload ; sudo systemctl restart gunicorn nginx