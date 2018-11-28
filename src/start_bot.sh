#!/bin/sh
mkdir ~/.ssh
echo $KNOWN_HOSTS > ~/.ssh/known_hosts

echo $SSH_KEY > ./tmp
tr '_' '\n' < ./tmp > ./id_rsa
chmod 600 ./id_rsa
rm ./tmp

echo Manager Parameters: $@

CMD="bash start_bot.sh $@"
echo CMD: $CMD

ssh -tt -i ./id_rsa $P_USER@$IP bash start_bot.sh $@