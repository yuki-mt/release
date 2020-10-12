username=$1
if [ -z "$username" ]; then
  echo "need username"
  exit 1
fi

policies=$(aws iam list-attached-user-policies --user-name nick | jq -r '.AttachedPolicies[].PolicyArn')
for policy in $policies ; do
  aws iam detach-user-policy --user-name $username --policy-arn $policy
done

access_keys=$(aws iam list-access-keys --user-name nick | jq -r '.AccessKeyMetadata[].AccessKeyId')
for key in $access_keys ; do
  aws iam delete-access-key --user-name $username --access-key-id $key
done

aws iam delete-login-profile --user-name $username
aws iam delete-user --user-name $username
