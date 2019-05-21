#!/bin/sh

cat /var/log/secure | grep -w 'ec2-user :'
