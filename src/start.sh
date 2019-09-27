#!/bin/sh

echo $SSH_KEY > ./tmp
tr '_' '\n' < ./tmp > ./id_rsa
chmod 600 ./id_rsa
rm ./tmp

echo sleep 30
sleep 30

/usr/local/bin/gunicorn --workers=10 --timeout 600 -b :$1 server:app