#!/bin/sh
set -e

username=$1
host=$2
dir=$3
css_dir=$4
js_dir=$5
user_dir=$6

sudo chmod 755 $HOME/.ssh/config
eval `ssh-agent`
ssh-add $HOME/.ssh/id_rsa

ssh $username@$host -p 6636 sh << SHELL
  cd $dir
  git reset --hard HEAD
  git checkout master
  git pull
  java -jar $user_dir/.jdk/yuicompressor.jar -o '.css$:.css' $css_dir/*.css
  java -jar $user_dir/.jdk/yuicompressor.jar -o '.js$:.js' $js_dir/*.js
SHELL
