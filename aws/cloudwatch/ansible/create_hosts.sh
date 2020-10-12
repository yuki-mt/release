export AWS_DEFAULT_REGION=$1

# get all running instances
ip_addresses=`aws ec2 describe-instances \
  --filters Name=instance-state-code,Values=16 \
  --query "Reservations[*].Instances[*].PublicIpAddress" \
  | jq -r '.[][]'`

cat - << EOS > hosts
[all]
$ip_addresses
EOS
