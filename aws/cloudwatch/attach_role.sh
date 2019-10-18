export AWS_DEFAULT_REGION=$1

# get all running instances
instance_ids=`aws ec2 describe-instances \
  --filters Name=instance-state-code,Values=16 \
  --query "Reservations[*].Instances[*].InstanceId" \
  | jq -r '.[][]'`

for instance_id in $instance_ids ; do
  aws ec2 associate-iam-instance-profile \
    --instance-id $instance_id \
    --iam-instance-profile Name=ec2-ssm-cloudwatch-agent
done
