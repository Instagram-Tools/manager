#!/bin/bash


sudo docker rm /selenium
sudo docker run -d --net=bridge --name selenium selenium/standalone-chrome:3.141.59

echo Composition Parameters: $@
INSTA_USER=$2
INSTA_PW=$3

echo "Composition sudo docker stop /$INSTA_USER"
sudo docker stop /$INSTA_USER
echo "Composition sudo docker rm /$INSTA_USER"
sudo docker rm /$INSTA_USER

SETTINGS=${1//' '/''}


CMD="sudo docker run -d -v ~/logs:/code/logs --net=bridge --link selenium:selenium -e SELENIUM=selenium --name $INSTA_USER -e ENV=$SETTINGS -e INSTA_USER=$INSTA_USER -e INSTA_PW=$INSTA_PW instagramtools/web sh ./wait-for-selenium.sh http://selenium:4444/wd/hub -- python docker_quickstart.py"
echo Composition CMD: $CMD

$CMD
