set -eu

# Before start

# mkdir ~/workspace
# sudo yum update -y
# sudo yum install -y zsh git
# sudo passwd <YOUR_USERNAME>
# sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
# sed -i -e 's/^alias.*//' ~/.oh-my-zsh/plugins/git/git.plugin.zsh
# cd ~/workspace
# git clone https://github.com/yuki-mt/scripts.git
# cd scripts/setup
# ./centos.sh

# git
./git.sh

# pyenv, rbenv, nvm
sudo yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel unzip bzip2 gcc wget htop lsof python-devel
git clone https://github.com/sstephenson/rbenv.git ~/.rbenv
git clone https://github.com/sstephenson/ruby-build.git ~/.rbenv/plugins/ruby-build
git clone git://github.com/creationix/nvm.git ~/.nvm
git clone https://github.com/yyuu/pyenv.git ~/.pyenv
cp ../files/centos/zshrc ~/.zshrc

export PATH="$HOME/.pyenv/shims:$HOME/.pyenv/bin:${PATH}"
pyenv install 3.6.8
pyenv global 3.6.8

source ~/.nvm/nvm.sh
nvm install v10.15.3

export PATH="$HOME/.rbenv/bin:$PATH"
eval "$(rbenv init -)"
rbenv install -v 2.6.3
rbenv rehash
rbenv global 2.6.3

source ~/.zshrc

# PHP
sudo yum install -y epel-release
sudo rpm -Uvh http://rpms.famillecollet.com/enterprise/remi-release-7.rpm
sudo yum install -y --enablerepo=epel,remi,remi-php73 php-opcache php-devel php-mbstring php-mysqlnd php-phpunit-PHPUnit php-pecl-xdebug php-gd php-intl php-fpm php-pdo php
curl -sS https://getcomposer.org/installer | php
sudo mv composer.phar /usr/local/bin/composer

# Python basic
pip install -U pip
pip install mypy flake8 jupyter nbextensions
mkdir -p $(jupyter --data-dir)/nbextensions
cd $(jupyter --data-dir)/nbextensions
git clone https://github.com/lambdalisue/jupyter-vim-binding vim_binding
jupyter nbextension enable vim_binding/vim_binding --sys-prefix
cd -

sudo yum remove -y vim*
sudo yum install -y ruby-devel lua-devel automake
git clone https://github.com/vim/vim.git
cd vim
./configure --prefix=/usr/local --with-features=huge --enable-multibyte --enable-rubyinterp --enable-luainterp --enable-cscope --enable-fail-if-missing --with-ruby-command=/usr/bin/ruby
make
sudo make install
cd ..
rm -rf vim
cp ../files/vimrc ~/.vimrc

# fzf
git clone https://github.com/junegunn/fzf.git ~/.fzf
~/.fzf/install

# MeCab
sudo yum install -y gcc-c++ xz
sudo rpm -ivh http://packages.groonga.org/centos/groonga-release-1.1.0-1.noarch.rpm
sudo yum install -y mecab mecab-ipadic
sudo yum install -y mecab-devel

# Docker
sudo yum remove -y docker docker-common docker-selinux docker-engine
sudo yum install -y yum-utils device-mapper-persistent-data lvm2
sudo yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
sudo yum makecache fast
sudo yum install -y docker-ce
# sudo systemctl start docker
# sudo systemctl enable docker

# MySQL, SQLite, Redis
sudo yum remove -y mariadb-libs
sudo rm -rf /var/lib/mysql/
sudo yum localinstall -y http://dev.mysql.com/get/mysql57-community-release-el7-7.noarch.rpm
sudo yum -y install mysql-community-server sqlite epel-release
sudo yum install -y redis
# sudo systemctl enable mysqld.service
# sudo systemctl start mysqld.service
# redis-server --version

# Nginx
sudo rpm -ivh http://nginx.org/packages/centos/7/noarch/RPMS/nginx-release-centos-7-0.el7.ngx.noarch.rpm
sudo yum -y update nginx-release-centos
sudo yum -y --enablerepo=nginx install nginx

# mail
sudo yum install -y nkf postfix
