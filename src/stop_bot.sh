#!/bin/sh
echo $KNOWN_HOSTS > ~/.ssh/known_hosts

echo $SSH_KEY > ./tmp
tr '_' '\n' < ./tmp > ./id_rsa
chmod 600 ./id_rsa
rm ./tmp

CMD="sudo docker rm -f /$1"
# echo CMD: $CMD

ssh -tt -i ./id_rsa $P_USER@$IP $CMD