#!/bin/sh

echo $SSH_KEY > ./tmp
tr '_' '\n' < ./tmp > ./id_rsa
chmod 600 ./id_rsa
rm ./tmp

IP=$1
shift

CMD="sudo docker ps --format 'table {{.Image}}' -f STATUS=running | grep -w web"
# echo CMD: $CMD

ssh -o StrictHostKeychecking=no -tt -i ./id_rsa $P_USER@$IP $CMD