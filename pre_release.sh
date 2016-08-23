#!/bin/sh
set -e

dir=$1

cwd=`pwd`
cd $dir
git reset --hard HEAD
git checkout develop
git pull origin develop
git checkout master
git merge develop
git push
git checkout develop
cd $cwd
