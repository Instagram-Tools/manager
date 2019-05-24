#!/bin/sh

echo $SSH_KEY > ./tmp
tr '_' '\n' < ./tmp > ./id_rsa
chmod 600 ./id_rsa
rm ./tmp

sleep 300

/usr/local/bin/gunicorn -b :$1 server:app & python start.py