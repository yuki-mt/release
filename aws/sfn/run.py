"""
Run a created state machine with some inputs
"""

import boto3
import json

account_num = 'xxx'
ARN = f"arn:aws:states:ap-northeast-1:{account_num}:stateMachine:test"


def main():
    command = {
        'task1_cmd': ['-a', '100'],
        'task2_cmd': ['-b', '110'],
        'task1_foo': ['-a', '100'],
        'task2_foo': ['-b', '110'],
        'task1_xx': ['-a', '100'],
        'task2_xx': ['-b', '110'],
    }
    state_input = json.dumps({'command': command}, indent=2, sort_keys=True)
    response = boto3.client('stepfunctions').start_execution(
        stateMachineArn=ARN,
        input=state_input
    )
    execution_arn = response['executionArn']
    print(
        'See progress in :',
        ('https://ap-northeast-1.console.aws.amazon.com/states/home?'
         f'region=ap-northeast-1#/executions/details/{execution_arn}')
    )


if __name__ == '__main__':
    main()
