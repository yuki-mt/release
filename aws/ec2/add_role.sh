"""
Add role to all EC2 instances
"""
role_name=$1
if [ -z "$role_name" ]; then
  echo "need role_name"
  exit 1
fi

for region in "us-west-2" "ap-northeast-1" ; do
  echo $region
  attached_ids=`aws --region $region ec2 describe-iam-instance-profile-associations --query 'IamInstanceProfileAssociations[].InstanceId' | jq -r '.[]'`
  all_ids=`aws --region $region ec2 describe-instances --query 'Reservations[].Instances[].InstanceId' | jq -r '.[]'`
  ids_to_attach=`echo -e $all_ids"\n"$attached_ids | sort | uniq -u`
  for id in $ids_to_attach ; do
    if [ -z "$id" ]; then
      continue
    fi
    aws --region $region ec2 associate-iam-instance-profile --instance-id $id --iam-instance-profile Name=$role_name
  done
done
