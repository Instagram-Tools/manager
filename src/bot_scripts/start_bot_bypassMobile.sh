#!/bin/bash

sudo service docker start
sudo service docker status

sudo docker pull instagramtools/web

# Delete all images
sudo docker rmi $(sudo docker images -q)

echo "Composition sudo docker stop /selenium"
sudo docker stop /selenium
echo "Composition sudo docker rm /selenium"
sudo docker rm /selenium
echo "Composition start /selenium"
sudo docker run -d --net=bridge --shm-size=128M --name selenium selenium/standalone-chrome:3.141.59

echo Composition Parameters: $@
INSTA_USER=$2
INSTA_PW=$3

echo "Composition sudo docker stop /bot"
sudo docker stop /bot
echo "Composition sudo docker rm /bot"
sudo docker rm /bot

SETTINGS=${1//' '/''}


CMD="sudo docker run -d -v /home/ec2-user/logs:/root/InstaPy/logs -v /home/ec2-user/db:/root/InstaPy/db --net=bridge --link selenium:selenium -e bypass_suspicious_attempt=True -e bypass_with_mobile=True -e SELENIUM=selenium --name bot -e ENV=$SETTINGS -e INSTA_USER=$INSTA_USER -e INSTA_PW=$INSTA_PW instagramtools/web sh ./wait-for-selenium.sh http://selenium:4444/wd/hub -- python docker_quickstart.py"
echo Composition CMD: $CMD

$CMD