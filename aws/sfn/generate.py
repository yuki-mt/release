"""
Create a state machine to run multiple ECS tasks
"""

import json
import boto3
from time import sleep

from template import base, branch, parallel, task

TASK1_REVISION = 5
TASK2_REVISION = 1

# need CloudWatchEventFullAccess & ECS run task
STATE_MACHINE_ROLEARN = 'arn:aws:iam::xxx'

def create_state_machine(definition: dict):
    name = "test"
    arn = f"arn:aws:states:ap-northeast-1:<YOUR_ACCOUNT>:stateMachine:{name}"
    client = boto3.client('stepfunctions')

    def _create():
        client.create_state_machine(
            name=name,
            definition=json.dumps(definition, indent=2, sort_keys=True),
            roleArn=STATE_MACHINE_ROLEARN
        )

    try:
        _create()
    except client.exceptions.StateMachineAlreadyExists:
        client.delete_state_machine(stateMachineArn=arn)
        print('deleting an old state machine...')
        sleep(60)
        _create()

def generate_predict_branch(category: str) -> dict:
    start_name = f'Start {category}'
    end_name = f'End {category}'
    return branch.get_json(start_name, {
        start_name: task.get_json('task1', TASK1_REVISION,
                                  f'task1_{category.lower()}', end_name),
        end_name: task.get_json('task2', TASK2_REVISION,
                                f'task2_{category.lower()}', None),
    })

def main():
    states = {
        'Task 1': task.get_json('task1', TASK1_REVISION, 'task1_cmd', 'Parallel Tasks'),
        'Parallel Tasks': parallel.get_json([
            generate_predict_branch('Foo'),
            generate_predict_branch('XX'),
        ], 'Task 2'),
        'Task 2': task.get_json('task2', TASK2_REVISION, 'task2_cmd', None),
    }
    create_state_machine(base.get_json('Task 1', states))


if __name__ == '__main__':
    main()
