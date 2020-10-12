"""
Add user with policy
"""
username=$1
if [ -z "$username" ]; then
  echo "need username"
  exit 1
fi

policies="
policy_arn
"

auth_info=`aws iam create-access-key --user-name $username`
access_key=`echo $auth_info | jq -r '.AccessKey.AccessKeyId'`
secret_key=`echo $auth_info | jq -r '.AccessKey.SecretAccessKey'`
for policy in $policies ; do
  aws iam attach-user-policy --user-name $username --policy-arn $policy
done

echo "
The following is your AWS account info
\`\`\`
username: $username
access key: $access_key
secret key: $secret_key
\`\`\` " | pbcopy
