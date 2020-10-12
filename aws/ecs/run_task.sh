#!/bin/bash

args=${1-''}
revision=1

aws ecs run-task \
  --cluster arn:aws:ecs:$REGION:$ACCOUNT_ID:cluster/$CLUSTER_NAME \
  --task-definition arn:aws:ecs:$REGION:$ACCOUNT_ID:task-definition/$TASK_DEF_NAME:$revision \
  --network-configuration "awsvpcConfiguration={subnets=[$SUBNET_ID1, $SUBNET_ID2],assignPublicIp=ENABLED}" \
  --launch-type FARGATE \
  --count 1 \
  --overrides "{
    \"containerOverrides\": [
        {
            \"name\": \"$CONTAINER_NAME\",
            \"command\": [\"$args\"]
        }
    ]
}"
