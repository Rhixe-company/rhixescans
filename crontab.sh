#!/bin/bash 

source env/bin/activate ; ./manage.py crawl ; sudo systemctl daemon-reload ; sudo systemctl reload gunicorn nginx