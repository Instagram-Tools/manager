#!/bin/bash

echo "" > nohup.out

sudo service docker start
# echo docker status: $(sudo service docker status)

# Delete all images
sudo docker rmi $(sudo docker images -q)

sudo docker pull instagramtools/web
sudo docker pull selenium/standalone-chrome:3.141.59

# echo "Composition sudo docker stop /selenium"
sudo docker stop /selenium
# echo "Composition sudo docker rm /selenium"
sudo docker rm /selenium
# echo "Composition start /selenium"
sudo docker run -d --net=bridge --name selenium selenium/standalone-chrome:3.141.59

# echo Composition Parameters: $@
INSTA_USER=$2
INSTA_PW=$3
EMAIL=$4
EMAIL_API=$5

# echo "Composition sudo docker stop /bot"
sudo docker stop /bot
# echo "Composition sudo docker rm /bot"
sudo docker rm /bot

SETTINGS=${1//' '/''}


CMD="sudo docker run -d -v /home/ec2-user/logs:/root/InstaPy/logs -v /home/ec2-user/db:/root/InstaPy/db --net=bridge --link selenium:selenium -e EMAIL_API=$EMAIL_API --name bot -e ENV=$SETTINGS -e INSTA_USER=$INSTA_USER -e INSTA_PW=$INSTA_PW -e EMAIL=$EMAIL instagramtools/web sh ./wait-for-selenium.sh http://selenium:4444/wd/hub -- python docker_quickstart.py"
# echo Composition CMD: $CMD

$CMD

echo Start stopped_shutdown.sh for $INSTA_USER: $(nohup sudo bash ./stopped_shutdown.sh)