#!/bin/bash
"""
全てのインスタンスに指定のIAM Roleを付与する
"""
export AWS_DEFAULT_REGION=$1
role_name=$2

# get all running instances
instance_ids=`aws ec2 describe-instances \
  --filters Name=instance-state-code,Values=16 \
  --query "Reservations[*].Instances[*].InstanceId" \
  | jq -r '.[][]'`

for instance_id in $instance_ids ; do
  aws ec2 associate-iam-instance-profile \
    --instance-id $instance_id \
    --iam-instance-profile Name=$role_name
done
