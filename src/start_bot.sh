#!/bin/sh
echo $SSH_KEY > ./tmp
tr '_' '\n' < ./tmp > ./id_rsa
rm ./tmp

ssh -i ./id_rsa docker@$IP <<-"END_SSH"

    docker stop /$1
    docker rm /$1

    docker run -d --name $1 -e INSTA_USER=$1 -e INSTA_PW=$2 \
    -e ENV=$3 -v log_data:/code/logs instagramtools/web

END_SSH