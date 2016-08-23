#!/bin/sh
root_pw=$1
doc_root=$2
staging_doc_root=$3
domain=$4
exec_sudo(){
  echo "$root_pw" | sudo -S $1
}

#generate SSH key
ssh-keygen
exec_sudo "chmod 700 $HOME/.ssh"
exec_sudo "chmod 600 $HOME/.ssh/id_rsa.pub"

exec_sudo "cp files/nginx.repo /etc/yum.repos.d/nginx.repo"

# execute the common part
username=${HOME:6}
./centos.sh "$root_pw" $username $HOME

#send files in files direcotry
exec_sudo "cp files/php.ini /etc/php.ini"
exec_sudo "cp files/my.cnf /etc/my.cnf"
exec_sudo "chown -R $username:$username /var/www/"
mkdir -p $doc_root
mkdir -p $staging_doc_root
sed -e "s;DOCUMENT-ROOT;$doc_root;g" -e "s;STAGING-ROOT;$staging_doc_root;g" -e "s;YOUR-DOMAIN;$domain;g" files/httpd.conf > files/temp_httpd.conf
exec_sudo "mv files/temp_httpd.conf /etc/httpd/conf/httpd.conf"

cp files/zshrc $HOME/.zshrc
cp files/vimrc $HOME/.vimrc
cp -R files/dict $HOME/.vim/
cp files/config $HOME/.ssh/config
chmod 600 ~/.ssh/config
sed -e "s;DOC-ROOT;$doc_root;g" -e "s;DOMAIN-NAME;$domain;g" files/nginx.default.conf > files/temp_nginx.default.conf
sed -e "s;DOC-ROOT;$staging_doc_root;g" -e "s;DOMAIN-NAME;$domain;g" files/nginx.staging.conf > files/temp_nginx.staging.conf
exec_sudo "cp files/nginx.conf /etc/nginx/nginx.conf"
exec_sudo "mv files/temp_nginx.default.conf /etc/nginx/conf.d/default.conf"
exec_sudo "mv files/temp_nginx.staging.conf /etc/nginx/conf.d/staging.conf"
exec_sudo "cp files/www.conf /etc/php-fpm.d/www.conf"
exec_sudo "cp files/mecabrc /usr/local/etc/mecabrc"
exec_sudo "cp files/ld.so.conf /etc/ld.so.conf"
exec_sudo "ldconfig"

source $HOME/.zshrc
exec_sudo "service httpd restart"
exec_sudo "service mysqld restart"
exec_sudo "service nginx restart"
exec_sudo "service php-fpm restart"

