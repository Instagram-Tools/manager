#!/bin/sh
echo $SSH_KEY > ./tmp
tr '_' '\n' < ./tmp > ./id_rsa
chmod 600 ./id_rsa
rm ./tmp

JSON=$1
shift

echo Manager JSON: $JSON
echo Manager Parameters: $@

CMD="bash start_bot.sh '$JSON' $@"
echo Manager CMD: $CMD

ssh -o StrictHostKeychecking=no -tt -i ./id_rsa $P_USER@$IP "bash start_bot.sh '$JSON' $@"