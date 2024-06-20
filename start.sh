#!/bin/bash
exec gunicorn -c /home/yeshambn/mcc.backup.miracle44radio.com/gunicorn.conf.py main:app
