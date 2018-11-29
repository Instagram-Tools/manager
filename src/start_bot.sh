#!/bin/sh
echo $KNOWN_HOSTS > ~/.ssh/known_hosts

echo $SSH_KEY > ./tmp
tr '_' '\n' < ./tmp > ./id_rsa
chmod 600 ./id_rsa
rm ./tmp

STR=$1
JSON=${STR//'"'/'\"'}
JSON2=${JSON//'{'/'\{'}
JSON3=${JSON2//'}'/'\}'}
shift

echo Manager JSON: $JSON3
echo Manager Parameters: $@

CMD="bash start_bot.sh $JSON3 $@"
echo CMD: $CMD

ssh -tt -i ./id_rsa $P_USER@$IP $CMD