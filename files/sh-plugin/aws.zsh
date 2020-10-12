_get_name_tag() {
  local instance_json tags
  instance_json=$1
  tags=`echo $instance_json | jq '.Tags'`
  len=`echo $tags | jq length`
  for i in $( seq 0 $(($len - 1)) ); do
    key=`echo $tags | jq -r ".[$i].Key"`
    if [ "$key" = 'Name' ]; then
      value=`echo $tags | jq -r ".[$i].Value"`
      echo $value
      break
    fi
  done
}

_get_ip() {
  local ip_key
  # ip_key='.PrivateIpAddress'
  ip_key='.NetworkInterfaces[0].Association.PublicIp'
  echo $instance | jq -r "$ip_key"
}

_get_instances() {
  local region nested_instances instances instance name ip_address
  region=$1
  nested_instances=`aws --region $region ec2 describe-instances \
    --query 'Reservations[*].Instances[*]' \
    --filters Name=instance-state-name,Values=running`
  len=`echo $nested_instances | jq length`
  for i in $( seq 0 $(($len - 1)) ); do
    instances=`echo $nested_instances | jq ".[$i]"`
    inner_len=`echo $instances | jq length`
    for j in $( seq 0 $(($inner_len - 1)) ); do
      instance=`echo $instances | jq ".[$j]"`
      name=`_get_name_tag "$instance"`
      ip_address=`_get_ip "$instance"`
      echo "$region	$name	$ip_address"
    done
  done
}

update-ec2() {
  rm -f ~/.sh-plugin/ec2.txt
  for region in ap-northeast-1 ap-southeast-1 us-west-2 ; do
    _get_instances $region >> ~/.sh-plugin/ec2.txt
  done
}

sssh() {
  local region ip_address user
  row=`cat ~/.sh-plugin/ec2.txt | fzf`
  region=`echo $row | awk '{print $1}'`
  ip_address=`echo $row | awk '{print $3}'`

  case $region in
	  'ap-northeast-1') ssh_path='~/.ssh/tokyo.pem';;
	  'ap-southeast-1') ssh_path='~/.ssh/singapore.pem';;
	  'us-west-2') ssh_path='~/.ssh/oregon.pem';;
	  *)
      echo "the region does not support"
      exit 1
  esac
  echo -n "user[ubuntu]: "
  read user
  user=${user:-"ubuntu"}
  cmd="ssh -i $ssh_path $user@$ip_address"
  echo ": `date +%s`:0;$cmd" >> ~/.zsh_history
  eval $cmd
}

find-ec2() {
  local region ip_address user
  row=`cat ~/.sh-plugin/ec2.txt | fzf`
  region=`echo $row | awk '{print $1}'`
  ip_address=`echo $row | awk '{print $3}'`
  open https://$region.console.aws.amazon.com/ec2/v2/home#Instances:search=$ip_address
}
