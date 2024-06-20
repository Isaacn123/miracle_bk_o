#!/bin/bash
source /home/yeshambn/virtualenv/mcc.backup.miracle44radio.com/3.9/bin/activate 
# exec gunicorn -c /home/yeshambn/mcc.backup.miracle44radio.com/gunicorn.conf.py main:app
exec gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app

