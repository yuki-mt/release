#!/bin/sh
root_pw=$1
username=$2
doc_root=$3
host=$4
staging_doc_root=$5
domain=$6

#set user_dir
if [ "$username" = root ]
then
  user_dir=/root
else
  user_dir=/home/$username
fi

#create files to be sent
sed -e "s;DOCUMENT-ROOT;$doc_root;g" -e "s;YOUR-DOMAIN;$domain;g" -e "s;STAGING-ROOT;$staging_doc_root;g" files/httpd.conf > files/temp_httpd.conf
sed -e "s;DOC-ROOT;$doc_root;g" -e "s;DOMAIN-NAME;$domain;g" files/nginx.remote.default.conf > files/temp_nginx.remote.default.conf
sed -e "s;DOC-ROOT;$staging_doc_root;g" -e "s;DOMAIN-NAME;$domain;g" files/nginx.staging.conf > files/temp_nginx.staging.conf
sed -e "s;YOUR-DOMAIN;$domain;g" files/iptables > files/temp_iptables
cp ~/.ssh/id_rsa.pub files/
#send files
tar cvf files.tar files
scp files.tar root@$host:$user_dir/files.tar
rm files/bash_profile_remote files/temp_httpd.conf files/id_rsa.pub files/temp_iptables

ssh root@$host sh <<SHELL
  tar xvf $user_dir/files.tar
  mv files/nginx.repo /etc/yum.repo.d/nginx.repo
SHELL

ssh $username@$host "sh -s $root_pw $username $user_dir"< ./centos.sh 

ssh root@$host sh <<SHELL
  #setting for ssh
  service sshd start
  chkconfig sshd on
  mkdir -p $user_dir/.ssh
  chmod 700 $user_dir/.ssh
  chown -R $username $user_dir/.ssh
  #send files
  mv files/php.ini /etc/php.ini
  cat files/id_rsa.pub >> $user_dir/.ssh/authorized_keys
  mkdir -p $doc_root
  mv files/my.cnf /etc/my.cnf
  mv files/temp_httpd.conf /etc/httpd/conf/httpd.conf
  mv files/zshrc $use_dir/.zshrc
  source $user_dir/.zshrc
  mv files/vimrc $use_dir/.vimrc
  mv files/temp_iptables /etc/sysconfig/iptables
  mv files/sshd_config /etc/ssh/sshd_config
  mv files/nginx.conf /etc/nginx/nginx.conf
  mv files/temp_nginx.remote.default.conf /etc/nginx/conf.d/default.conf
  mv files/temp_nginx.staging.conf /etc/nginx/conf.d/staging.conf
  mv files/www.conf /etc/php-fpm.d/www.conf
  mv files/mecabrc /usr/local/etc/mecabrc
  mv files/id.so.conf /etc/ld.so.conf
  ldconfig

  rm $user_dir/files.tar
  rm -rf files
  service httpd restart
  service sshd restart
  service mysqld restart
  service nginx restart
  service php-fpm restart
  chkconfig httpd on
  chkconfig mysqld on
  chkconfig redis on
  chkconfig nginx on
  chkconfig php-fpm on
SHELL
