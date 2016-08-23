#!/bin/sh
set -e

username=$1
host=$2
dir=$3

sudo chmod 755 $HOME/.ssh/config
eval `ssh-agent`
ssh-add $HOME/.ssh/id_rsa

ssh $username@$host -p 6636 sh << SHELL
  cd $dir
  git reset --hard HEAD
  git checkout develop
  git pull
  mv .htaccess web/
  rm web/assets/js/sdk.js
SHELL
