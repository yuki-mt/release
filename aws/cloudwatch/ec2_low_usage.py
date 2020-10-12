"""
EC2の指定のinstanceの指定のメトリクスが閾値を超えているかを出力
"""
import boto3
from typing import Iterator

from usage import get_metric_values


def get_ec2_metrics(client, metric: str, instance_id: str,
                    period: int = 300, unit: str = 'Percent',
                    interval_hours: int = 24) -> Iterator[float]:
    return get_metric_values(
        client, 'AWS/EC2', metric,
        {'Name': 'InstanceId', 'Value': instance_id},
        period, unit, interval_hours)


def main():
    instance_id = 'i-xxx'
    metric_name = 'CPUUtilization'
    total_threshold = 100
    threshold = 0.05

    client = boto3.client('cloudwatch')

    values = list(get_ec2_metrics(client, metric_name, instance_id))
    avg = sum(values) / len(values)

    if len(values) > total_threshold:
        if avg < threshold:
            print(f'{metric_name} is too low. instance-id: {instance_id}. average: {avg}')
        else:
            print(f'{metric_name} is moderate. instance-id: {instance_id}. average: {avg}')
    else:
        print(f'number of values is too few to judge. metric-name: {metric_name}. instance-id: {instance_id}')


if __name__ == '__main__':
    main()
