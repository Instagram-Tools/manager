#!/bin/sh

IP=$1
shift

INSTA_USER=$1

# echo Manager JSON: $JSON
# echo Manager Parameters: $@

CMD="bash start_bot.sh '$JSON' $@"
# echo Manager CMD: $CMD

scp -o StrictHostKeychecking=no -i ./id_rsa -r ./bot_scripts $P_USER@$IP:
ssh -o StrictHostKeychecking=no -i ./id_rsa $P_USER@$IP "bash bot_scripts/first_login_bot.sh $@"

echo Manager started first Login Bot: $INSTA_USER