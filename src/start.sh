#!/bin/sh

/usr/local/bin/gunicorn -t 300 --workers=10 -b :$1 server:app & python start.py