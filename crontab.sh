#!/bin/bash 

source env/bin/activate ; ./manage.py crawlasura ; sudo systemctl daemon-reload ; sudo systemctl restart gunicorn nginx