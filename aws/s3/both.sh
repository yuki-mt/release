#!/bin/bash
"""
create S3 read&write policy & user
"""
bucket_name=$1
do_add_user=$2
if [ -z "$bucket_name" ]; then
  echo "need bucket_name"
  exit 1
fi

content=`sed -e "s/YOUR_BUCKET/$bucket_name/" readwrite.json`
policy=`aws iam create-policy --policy-name "s3-$bucket_name-read-write" \
  --policy-document "$content" | jq -r '.Policy.Arn'`

if [ "$do_add_user" == "true" ]; then
  username="s3-$bucket_name-read-write"
  aws iam create-user --user-name $username
  auth_info=`aws iam create-access-key --user-name $username`
  access_key=`echo $auth_info | jq -r '.AccessKey.AccessKeyId'`
  secret_key=`echo $auth_info | jq -r '.AccessKey.SecretAccessKey'`
  aws iam attach-user-policy --user-name $username --policy-arn $policy

  echo "
The following is your AWS account info for S3
\`\`\`
username: $username
access key: $access_key
secret key: $secret_key
\`\`\` " | pbcopy
else
  echo $policy | pbcopy
  echo "copyed ARN"
fi
