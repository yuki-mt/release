#!/bin/bash
"""
Delete unused Key-Pair
"""
region=$1
case $region in
 ap-northeast-1)
   region_code=$region
   ;;
 us-west-2)
   region_code=$region
   ;;
 ap-southeast-1)
   region_code=$region
   ;;
 t*)
   region_code='ap-northeast-1'
   ;;
 o*)
   region_code='us-west-2'
   ;;
 s*)
   region_code='ap-southeast-1'
   ;;
 *)
   echo 'invalid region'
   exit 1
   ;;
esac

echo 'delete the unused KayPair'
aws --region $region_code ec2 describe-instances | jq -r '.Reservations[].Instances[].KeyName' | sort | uniq > used_keys.txt
aws --region $region_code ec2 describe-key-pairs | jq -r '.KeyPairs[].KeyName' | sort | uniq > keys.txt

for key in `comm -13 used_keys.txt keys.txt` ; do
  aws ec2 delete-key-pair --key-name $key
done

rm keys.txt used_keys.txt
