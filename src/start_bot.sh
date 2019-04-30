#!/bin/sh
echo $SSH_KEY > ./tmp
tr '_' '\n' < ./tmp > ./id_rsa
chmod 600 ./id_rsa
rm ./tmp

IP=$1
shift

JSON=$1
shift

INSTA_USER=$1

# echo Manager JSON: $JSON
# echo Manager Parameters: $@

CMD="bash start_bot.sh '$JSON' $@"
# echo Manager CMD: $CMD

scp -o StrictHostKeychecking=no -i ./id_rsa -r ./bot_scripts $P_USER@$IP:
ssh -o StrictHostKeychecking=no -tt -i ./id_rsa $P_USER@$IP "bash bot_scripts/start_bot.sh '$JSON' $@"

echo Manager started Bot: $INSTA_USER