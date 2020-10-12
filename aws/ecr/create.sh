#!/bin/bash
"""
create ECR repos as batch
"""

repos="
repo1
repo2
"

prefix="namespace/"

for repo in $repos; do
  aws ecr create-repository \
    --repository-name "$prefix$repo" \
    --image-tag-mutability IMMUTABLE
  aws ecr put-lifecycle-policy \
    --repository-name "$prefix$repo" \
    --lifecycle-policy-text '{
      "rules": [
        {
          "action": {
            "type": "expire"
          },
          "selection": {
            "countType": "imageCountMoreThan",
            "countNumber": 50,
            "tagStatus": "any"
          },
          "rulePriority": 1
        }
      ]
    }'
done
