old_name=$1
new_name=$2
account_id=`aws sts get-caller-identity --query Account --output text`
if [ -z "$old_name" ]; then
  echo "need old policy name"
  exit 1
fi
if [ -z "$new_name" ]; then
  echo "need new policy name"
  exit 1
fi

users=`aws iam list-users | jq '.Users'`
len=`echo $users | jq '. | length'`

for i in `seq 0 $(expr $len - 1)` ; do
  username=`echo $users | jq -r ".[$i].UserName"`
  policy_exist=`aws iam list-attached-user-policies --user-name $username | grep $old_name`
  if [ -n "$policy_exist" ] ; then
    echo "change $username"
    aws iam attach-user-policy --user-name $username --policy-arn "arn:aws:iam::$account_id:policy/$new_name"
    aws iam detach-user-policy --user-name $username --policy-arn "arn:aws:iam::$account_id:policy/$old_name"
  fi
done
