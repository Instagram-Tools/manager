#!/bin/bash

ssh -o StrictHostKeychecking=no -tt -i bot.pem ec2-user@$1
