#!/bin/sh

/usr/local/bin/gunicorn -b :$1 server:app & python start.py