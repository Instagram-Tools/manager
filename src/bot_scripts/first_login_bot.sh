#!/bin/bash

echo "" > nohup.out

sudo service docker start
# echo docker status: $(sudo service docker status)

# Delete all images
sudo docker rmi $(sudo docker images -q)

sudo docker pull instagramtools/web
sudo docker pull selenium/standalone-chrome:3.141.59

# echo "Composition sudo docker stop /selenium"
#sudo docker stop /selenium
# echo "Composition sudo docker rm /selenium"
#sudo docker rm /selenium
# echo "Composition start /selenium"
sudo docker run -d --net=bridge --shm-size=128M --name selenium selenium/standalone-chrome:3.141.59
sudo docker start /selenium

# echo Composition Parameters: $@
INSTA_USER=$1
INSTA_PW=$2
EMAIL=$3
API=$4
SEC_CODE=$5

# echo "Composition sudo docker stop /bot_login"
sudo docker stop /bot_login
# echo "Composition sudo docker rm /bot_login"
sudo docker rm /bot_login


CMD="sudo docker run -d -v /home/ec2-user/logs:/root/InstaPy/logs -v /home/ec2-user/db:/root/InstaPy/db --net=bridge --link selenium:selenium -e API=$API --name bot_login -e INSTA_USER=$INSTA_USER -e INSTA_PW=$INSTA_PW -e EMAIL=$EMAIL -e SEC_CODE=$SEC_CODE instagramtools/web sh ./wait-for-selenium.sh http://selenium:4444/wd/hub -- python docker_tryLogin.py"
# echo Composition CMD: $CMD

$CMD

echo Start stopped_shutdown.sh for $INSTA_USER:
nohup bash ./stopped_shutdown.sh 0<&- &> nohup.out &