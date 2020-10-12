import json
from typing import Optional

template = """
{
  "Type": "Task",
  "Resource": "arn:aws:states:::ecs:runTask.sync",
  "ResultPath": "$.result",
  "OutputPath": "$",
  "InputPath": "$",
  "Parameters": {
    "LaunchType": "FARGATE",
    "Cluster": "<YOUR_CLUSTER_ARN>",
    "TaskDefinition": "arn:aws:ecs:ap-northeast-1:<ACCOUNT_ID>:task-definition/<NAME>:<REVISION>",
    "Overrides": {
      "ContainerOverrides": [
        {
          "Name": "<NAME>",
          "Command.$": "$.command.<CMD>"
        }
      ]
    },
    "NetworkConfiguration": {
      "AwsvpcConfiguration": {
        "Subnets": [
          "subnet-xxx"
        ],
        "AssignPublicIp": "ENABLED"
      }
    }
  }
}
"""


def get_json(name: str, revision: int, cmd: str, next_task: Optional[str]) -> dict:
    json_str = template\
        .replace('<NAME>', name)\
        .replace('<REVISION>', str(revision))\
        .replace('<CMD>', cmd)
    output = json.loads(json_str)
    if next_task is None:
        output['End'] = True
    else:
        output['Next'] = next_task
    return output
