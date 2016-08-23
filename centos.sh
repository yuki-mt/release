#!/bin/sh
set -e
root_pw=$1
username=$2
user_dir=$3

exec_sudo(){
  echo "$root_pw" | sudo -S $1
}

git config --global color.ui true

exec_sudo "yum -y update"

exec_sudo "yum -y install zsh"
#oh-my-zsh
sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"

sed -e 's/^alias.*//' ~/.oh-my-zsh/plugins/git/git.plugin.zsh > git.plugin.zsh.temp
mv git.plugin.zsh.temp ~/.oh-my-zsh/plugins/git/git.plugin.zsh

#install some basic ones
exec_sudo "yum -y install epel-release vim man httpd libselinux-python nginx"

#install remi, epel
exec_sudo "rpm -Uvh --force http://rpms.famillecollet.com/enterprise/remi-release-6.rpm"

#install php
exec_sudo "yum -y install --enablerepo=remi gd-last"
exec_sudo "yum -y install --enablerepo=remi-php56 php php-common php-pdo php-cli php-devel php-mysqlnd php-mbstring php-gd php-fpm php-pecl-redis"

#install sass
exec_sudo "yum -y install rubygems"
exec_sudo "gem install sass"

#install ruby and mysql-server
exec_sudo "yum -y install --enablerepo=remi,epel mysql-server gcc openssl openssl-devel rpm-build gcc-c++ bzip2 bzip2-devel sqlite-devel libtool zlib zlib-devel ncurses-devel gdbm-devel readline readline-devel libyaml-devel libffi-devel bison redis python-devel libxml2-devel libxslt-devel"
mkdir -p $user_dir/.rbenv
git clone https://github.com/sstephenson/rbenv.git $user_dir/.rbenv
# takes a long time
mkdir -p $user_dir/.rbenv/plugins
git clone git://github.com/sstephenson/ruby-build.git $user_dir/.rbenv/plugins/ruby-build
$user_dir/.rbenv/bin/rbenv install 2.2.2
$user_dir/.rbenv/bin/rbenv global 2.2.2

sh_dir=`pwd`
cd $user_dir

#install nodejs
exec_sudo "yum -y install nodejs npm --enablerepo=epel"
curl https://raw.githubusercontent.com/creationix/nvm/v0.13.1/install.sh | bash
source ~/.bash_profile
nvm install v6.1.0
nvm alias default v6.1.0

npm install -g node-gyp express forever typescript typescript-tools


#install python, scikit-learn, scrapy
git clone git://github.com/yyuu/pyenv.git .pyenv
mkdir -p .pyenv/versions .pyenv/shims
cd .pyenv/plugins/
git clone git://github.com/yyuu/pyenv-virtualenv.git
export PATH="$user_dir/.pyenv/shims:$user_dir/.pyenv/bin:${PATH}"
pyenv install anaconda3-2.5.0
pyenv global anaconda3-2.5.0
pip install -U pip
pip install scrapy
exec_sudo "yum -y  --enablerepo=remi,epel install python-devel mysql-devel"
pip install mysqlclient 
#pip install service_identity

#install java
cd $user_dir
wget --no-check-certificate --no-cookies --header "Cookie: oraclelicense=accept-securebackup-cookie" http://download.oracle.com/otn-pub/java/jdk/8u65-b17/jdk-8u65-linux-x64.rpm
exec_sudo "rpm -ivh jdk-8u65-linux-x64.rpm"

#download yuicompressor
mkdir .jdk
wget https://github.com/yui/yuicompressor/releases/download/v2.4.8/yuicompressor-2.4.8.jar -O $HOME/.jdk/yuicompressor.jar

#install mecab
wget http://mecab.googlecode.com/files/mecab-0.996.tar.gz
tar xvf mecab-0.996.tar.gz 
cd mecab-0.996/
./configure
make
make check
exec_sudo "make install"
cd ../
wget http://mecab.googlecode.com/files/mecab-ipadic-2.7.0-20070801.tar.gz 
tar xvf mecab-ipadic-2.7.0-20070801.tar.gz 
cd mecab-ipadic-2.7.0-20070801/
./configure --with-charset=utf8
make
exec_sudo "make install"
cd ../
exec_sudo "yum install -y mecab-devel make xz"
git clone --depth 1 https://github.com/neologd/mecab-ipadic-neologd.git
cd mecab-ipadic-neologd/seed
pyenv global anaconda3-2.5.0 
xz -dkv mecab-user-dict-seed.*.csv.xz
pyenv global 2.7.10
/usr/local/libexec/mecab/mecab-dict-index -d /usr/local/lib/mecab/dic/ipadic -u mecab-user-dict-seed.dic -f utf-8 -t utf-8 mecab-user-dict-seed.*.csv
exec_sudo "mv mecab-user-dict-seed.dic /usr/local/lib/mecab/dic/ipadic/"
cd $user_dir
rm -rf mecab-ipadic-neologd
pip install mecab-python3

#go back to release directory
cd $sh_dir 

#change owner
exec_sudo "chown -R $username /var/www/html"


#service
start_service(){
  for s in $@
  do
    exec_sudo "service $s start"
    exec_sudo "chkconfig $s on"
  done
}

start_service httpd mysqld nginx php-fpm redis
