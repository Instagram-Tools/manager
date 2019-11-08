#!/bin/sh

RUNNING="RUNNING"

while [ "$RUNNING" ]
do
    sleep 300
    RUNNING="$(sudo docker ps --format 'table {{.Image}}' -f STATUS=running | grep -w instagramtools)"
done

echo SHUTDOWN because Bot stopped: $1
sudo /sbin/shutdown -h now