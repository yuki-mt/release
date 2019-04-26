set -eu

# Before start

## mkdir ~/workspace
## yum update -y 
## yum install -y zsh git
## sh -c "$(curl -fsSL https://raw.github.com/robbyrussell/oh-my-zsh/master/tools/install.sh)"
## sed -i -e 's/^alias.*//' ~/.oh-my-zsh/plugins/git/git.plugin.zsh
## ssh-keygen
## cat ~/.ssh/id_rsa.pub # register to Github
## cd ~/workspace
## git clone git@github.com:yuki-mt/scripts.git
## cd scripts/setup
## ./centos.sh

# git
./git.sh

# pyenv, rbenv, nvm
yum -y install zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel unzip bzip2 
git clone https://github.com/sstephenson/rbenv.git ~/.rbenv
git clone https://github.com/sstephenson/ruby-build.git ~/.rbenv/plugins/ruby-build
git clone git://github.com/creationix/nvm.git ~/.nvm
git clone https://github.com/yyuu/pyenv.git ~/.pyenv
cp ../files/centos/zshrc ~/.zshrc
source ~/.zshrc
pyenv install 3.6.8
pyenv global 3.6.8
rbenv install -v 2.6.3
rbenv rehash
rbenv global 2.6.3
nvm install v10.15.3

# Python basic
pip install -U pip
pip install mypy flake8 jupyter nbextensions
mkdir -p $(jupyter --data-dir)/nbextensions
cd $(jupyter --data-dir)/nbextensions
git clone https://github.com/lambdalisue/jupyter-vim-binding vim_binding
jupyter nbextension enable vim_binding/vim_binding --sys-prefix

# vim
yum update -y vim*
yum install -y vim
git clone --depth=1 https://github.com/universal-ctags/ctags.git
cd ctags
./autogen.sh
./configure
make
make install
cd ..
rm -rf ctags
./vim.sh

# fzf
git clone https://github.com/junegunn/fzf.git ~/.fzf
~/.fzf/install

# MeCab
yum install -y gcc-c++ xz
rpm -ivh http://packages.groonga.org/centos/groonga-release-1.1.0-1.noarch.rpm
yum install -y mecab mecab-ipadic
yum install -y mecab-devel

# Docker
yum remove -y docker docker-common docker-selinux docker-engine
yum install -y yum-utils device-mapper-persistent-data lvm2
yum-config-manager --add-repo https://download.docker.com/linux/centos/docker-ce.repo
yum makecache fast
yum install docker-ce
# systemctl start docker
# systemctl enable docker

# MySQL, SQLite, Redis
yum remove -y mariadb-libs
rm -rf /var/lib/mysql/
yum localinstall http://dev.mysql.com/get/mysql57-community-release-el7-7.noarch.rpm
yum -y install mysql-community-server sqlite epel-release
yum install -y redis
# systemctl enable mysqld.service
# systemctl start mysqld.service
# redis-server --version

# Nginx
rpm -ivh http://nginx.org/packages/centos/7/noarch/RPMS/nginx-release-centos-7-0.el7.ngx.noarch.rpm
yum -y update nginx-release-centos
yum -y --enablerepo=nginx install nginx
