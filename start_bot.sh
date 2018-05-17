#!/bin/bash

ssh -i $PATH_TO_SSH_KEY -p $SSH_PORT docker@$IP

docker stop /$1
docker rm /$1

docker-compose run -d --name $1 -e INSTA_USER=$1 -e INSTA_PW=$2 -e ENV=$3 web