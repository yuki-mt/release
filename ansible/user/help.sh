#!/bin/bash

echo "
- change IP address in hosts
- run
  ansible-playbook user.yml -u ubuntu --key-file ~/.ssh/oregon.pem -i hosts -e 'username=USER_NAME'
  or
  ansible-playbook key.yml -u ubuntu --key-file ~/.ssh/oregon.pem -i hosts -e 'key_path=\"\"' -e 'username=USERNAME'
"
