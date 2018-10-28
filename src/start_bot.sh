#!/bin/sh
mkdir ~/.ssh
echo $KNOWN_HOSTS > ~/.ssh/known_hosts

echo $SSH_KEY > ./tmp
tr '_' '\n' < ./tmp > ./id_rsa
chmod 600 ./id_rsa
rm ./tmp

STR=$1
JSON=${STR//'"'/'\"'}
shift

echo Manager JSON: ${JSON}
echo Manager Parameters: $@

ssh -tt -i ./id_rsa $P_USER@$IP "sh start_bot.sh $JSON $@"