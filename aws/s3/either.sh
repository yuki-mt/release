#!/bin/bash
"""
create S3 read-only policy & user
"""
bucket_name=$1
type=$2
if [ -z "$bucket_name" ]; then
  echo "need bucket_name"
  exit 1
fi
case $type in
	r*) type="read";;
	w*) type=write;;
	*)
    echo "need type (w or r)"
    exit 1
	  ;;
esac

content=`sed -e "s/YOUR_BUCKET/$bucket_name/" ${type}_only.json`
policy=`aws iam create-policy --policy-name "s3-$bucket_name-${type}only" \
  --policy-document "$content" | jq -r '.Policy.Arn'`

username="s3-$bucket_name-${type}only"
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
